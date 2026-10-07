"""Import content/projects/<name>/project.docx and content/research/<name>/research.docx."""
import argparse
import hashlib
import json
import posixpath
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlparse
from zipfile import ZipFile

from local_editor import ROOT, SLUG, ContentStore, atomic_write, json_bytes, validate

NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main', 'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships', 'a': 'http://schemas.openxmlformats.org/drawingml/2006/main', 'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing'}
FIELDS = {'title', 'summary', 'context', 'role', 'order', 'featured', 'related research'}


def tag(name):
    prefix, local = name.split(':')
    return '{' + NS[prefix] + '}' + local


def parse_document(path):
    if path.suffix.lower() != '.docx':
        raise ValueError('Save the legacy .doc document as a .docx file in Word first.')
    if path.stat().st_size > 60 * 1024 * 1024:
        raise ValueError('Word documents must be smaller than 60 MB.')
    with ZipFile(path) as archive:
        if sum(member.file_size for member in archive.infolist()) > 150 * 1024 * 1024:
            raise ValueError('The document contains too much unpacked content.')
        document = ET.fromstring(archive.read('word/document.xml'))
        if document.find('.//w:ins', NS) is not None or document.find('.//w:del', NS) is not None:
            raise ValueError('Accept or reject tracked changes in Word before importing.')
        rels = {}
        if 'word/_rels/document.xml.rels' in archive.namelist():
            rels = {item.attrib['Id']: item.attrib for item in ET.fromstring(archive.read('word/_rels/document.xml.rels'))}
        styles = {}
        if 'word/styles.xml' in archive.namelist():
            styles = {item.attrib.get(tag('w:styleId')): item for item in ET.fromstring(archive.read('word/styles.xml')).findall('w:style', NS)}
        numbering = {}
        if 'word/numbering.xml' in archive.namelist():
            numbers = ET.fromstring(archive.read('word/numbering.xml'))
            abstracts = {item.attrib.get(tag('w:abstractNumId')): item for item in numbers.findall('w:abstractNum', NS)}
            for item in numbers.findall('w:num', NS):
                abstract = item.find('w:abstractNumId', NS)
                if abstract is not None:
                    numbering[item.attrib.get(tag('w:numId'))] = abstracts.get(abstract.attrib.get(tag('w:val')))

        def style_of(paragraph):
            style = paragraph.find('w:pPr/w:pStyle', NS)
            return style.attrib.get(tag('w:val'), '') if style is not None else ''

        def list_prefix(paragraph, style):
            props = paragraph.find('w:pPr/w:numPr', NS)
            if props is None and styles.get(style) is not None:
                props = styles[style].find('w:pPr/w:numPr', NS)
            if props is None:
                return '1. ' if 'listnumber' in style.lower() else '- ' if 'listbullet' in style.lower() else ''
            identifier, level = props.find('w:numId', NS), props.find('w:ilvl', NS)
            abstract = numbering.get(identifier.attrib.get(tag('w:val'))) if identifier is not None else None
            depth = int(level.attrib.get(tag('w:val'), '0')) if level is not None else 0
            fmt = None
            if abstract is not None:
                entry = abstract.find(f'w:lvl[@w:ilvl="{depth}"]/w:numFmt', NS)
                fmt = entry.attrib.get(tag('w:val')) if entry is not None else None
            return '  ' * min(depth, 8) + ('- ' if fmt in (None, 'bullet') else '1. ')

        def inline(element):
            if element.tag == tag('w:r'):
                value = ''.join((child.text or '') if child.tag == tag('w:t') else '\n' if child.tag in (tag('w:br'), tag('w:cr')) else ' ' if child.tag == tag('w:tab') else '' for child in element)
                props = element.find('w:rPr', NS)
                if props is not None and value.strip():
                    for key, marker in [('w:i', '*'), ('w:b', '**')]:
                        prop = props.find(key, NS)
                        if prop is not None and prop.attrib.get(tag('w:val'), '1') not in ('0', 'false'):
                            value = marker + value + marker
                return value
            children = ''.join(inline(child) for child in element if child.tag not in (tag('w:pPr'), tag('w:rPr')))
            if element.tag == tag('w:hyperlink'):
                target = rels.get(element.attrib.get(tag('r:id')), {}).get('Target', '')
                if element.attrib.get(tag('w:anchor')):
                    target = '#' + element.attrib[tag('w:anchor')]
                if target and urlparse(target).scheme in ('', 'http', 'https', 'mailto', 'tel'):
                    target = target.replace(' ', '%20').replace('(', '%28').replace(')', '%29')
                    return '[' + children + '](' + target + ')'
            return children

        metadata, blocks, assets = {}, [], []
        heading, lines, started = '', [], False

        def flush():
            nonlocal heading, lines
            if heading or lines:
                body = ''
                for value in lines:
                    if body:
                        body += '\n' if value.lstrip().startswith(('- ', '1. ')) and body.splitlines()[-1].lstrip().startswith(('- ', '1. ')) else '\n\n'
                    body += value
                blocks.append({'type': 'text', 'heading': heading, 'body': body})
                heading, lines = '', []

        for paragraph in document.find('w:body', NS):
            if paragraph.tag == tag('w:tbl'):
                if paragraph.find('.//w:gridSpan', NS) is not None or paragraph.find('.//w:vMerge', NS) is not None:
                    raise ValueError('Use a simple table without merged cells.')
                if not started or paragraph.find('.//w:drawing', NS) is not None:
                    raise ValueError('Put simple text tables under a content heading, and keep pictures outside tables.')
                rows = [[ '<br>'.join(inline(p).strip() for p in cell.findall('w:p', NS)).replace('|', '\\|') for cell in row.findall('w:tc', NS)] for row in paragraph.findall('w:tr', NS)]
                if rows:
                    if len({len(row) for row in rows}) != 1:
                        raise ValueError('Use a table without merged cells.')
                    lines.append('\n'.join(['| ' + ' | '.join(rows[0]) + ' |', '| ' + ' | '.join(['---'] * len(rows[0])) + ' |'] + ['| ' + ' | '.join(row) + ' |' for row in rows[1:]]))
                continue
            if paragraph.tag != tag('w:p'):
                continue
            if paragraph.find('.//w:txbxContent', NS) is not None:
                raise ValueError('Use ordinary paragraphs rather than text boxes.')
            value = inline(paragraph).strip()
            style = style_of(paragraph)
            style_xml = styles.get(style)
            style_name = style_xml.find('w:name', NS) if style_xml is not None else None
            name = style_name.attrib.get(tag('w:val'), style) if style_name is not None else style
            if re.match(r'heading\s*[1-6]$', name, re.I):
                flush(); heading = value.replace('*', ''); started = True
                continue
            pictures = paragraph.findall('.//w:drawing', NS)
            if not started:
                plain = value.replace('*', '')
                key, separator, val = plain.partition(':')
                if separator and key.strip().lower() in FIELDS:
                    metadata[key.strip().lower()] = val.strip()
                elif plain and style.lower() not in ('title', 'subtitle') and not plain.lower().startswith('note:'):
                    raise ValueError('Place labelled metadata before the first Heading 1 section. Unexpected text: ' + plain[:80])
                if pictures:
                    raise ValueError('Insert pictures under a content heading.')
                continue
            if value and not pictures and blocks and blocks[-1]['type'] == 'image' and (style.lower() == 'caption' or value.lower().startswith(('caption:', 'alt:', 'image width:'))):
                key, separator, val = value.partition(':')
                if key.lower() == 'alt':
                    blocks[-1]['alt'] = val.strip()
                elif key.lower() == 'image width':
                    blocks[-1]['size'] = val.strip().lower()
                else:
                    blocks[-1]['caption'] = val.strip() if key.lower() == 'caption' and separator else value
                continue
            if value:
                lines.append(list_prefix(paragraph, style) + value)
            for drawing in pictures:
                blips = drawing.findall('.//a:blip', NS)
                if not blips:
                    raise ValueError('Convert charts and shapes into an inline picture before importing.')
                description = drawing.find('.//wp:docPr', NS)
                alt = description.attrib.get('descr', '') if description is not None else ''
                for blip in blips:
                    relation = rels.get(blip.attrib.get(tag('r:embed')), {})
                    member = posixpath.normpath(posixpath.join('word', relation.get('Target', '')))
                    if relation.get('TargetMode') == 'External' or not member.startswith('word/media/'):
                        raise ValueError('Embed pictures using Insert Pictures and In Line with Text.')
                    payload = archive.read(member)
                    suffix = Path(member).suffix.lower()
                    if suffix not in ('.png', '.jpg', '.jpeg', '.webp', '.gif'):
                        raise ValueError('Use PNG, JPEG, WebP, or GIF pictures.')
                    if len(payload) > 15 * 1024 * 1024:
                        raise ValueError('Each embedded image must be smaller than 15 MB.')
                    flush()
                    src = '/assets/images/imported/' + hashlib.sha256(payload).hexdigest()[:24] + suffix
                    blocks.append({'type': 'image', 'src': src, 'alt': alt, 'caption': '', 'size': 'full'})
                    assets.append((src, payload))
        flush()
        if '[REPLACE' in json.dumps({'metadata': metadata, 'blocks': blocks}).upper():
            raise ValueError('Replace all template placeholders before importing.')
        if not started:
            raise ValueError('Use Word Heading 1 styles for content section headings.')
        return metadata, blocks, assets


def import_folders(root=ROOT, force=False, only=None, dry_run=False):
    root = Path(root).resolve()
    store = ContentStore(root)
    current = store.read()
    manifest_path = root / 'local/document-imports.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf-8')) if manifest_path.exists() else {}
    imported, assets, hashes = [], [], dict(manifest)
    for kind, filename in [('projects', 'project.docx'), ('research', 'research.docx')]:
        base = root / 'content' / kind
        if not base.exists():
            continue
        for folder in sorted(base.iterdir()):
            if not folder.is_dir() or (only and folder.name != only):
                continue
            if not SLUG.fullmatch(folder.name):
                raise ValueError('Use lowercase letters, numbers, and hyphens in folder names: ' + folder.name)
            path = folder / filename
            if not path.is_file():
                if list(folder.glob('*.doc')):
                    raise ValueError(str(folder.relative_to(root)) + ': Save the .doc file as ' + filename + ' first.')
                continue
            relative = path.relative_to(root).as_posix()
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            if not force and manifest.get(relative) == digest:
                continue
            try:
                metadata, blocks, images = parse_document(path)
                if not metadata.get('title') or not metadata.get('summary'):
                    raise ValueError('Title and Summary metadata are required.')
                if kind == 'projects':
                    prior = current['projects'].get(folder.name, {})
                    featured = metadata.get('featured', str(prior.get('featured', False))).lower()
                    if featured not in ('yes', 'no', 'true', 'false'):
                        raise ValueError('Featured must be yes or no.')
                    current['projects'][folder.name] = {
                        'title': metadata['title'], 'summary': metadata['summary'],
                        'context': metadata.get('context', prior.get('context', '')),
                        'role': metadata.get('role', prior.get('role', '')),
                        'order': int(metadata.get('order', prior.get('order', len(current['projects']) + 1))),
                        'featured': featured in ('yes', 'true'),
                        'research_anchor': metadata.get('related research', prior.get('research_anchor', '')),
                        'blocks': blocks,
                    }
                else:
                    module = {'id': folder.name, 'title': metadata['title'], 'summary': metadata['summary'], 'blocks': blocks}
                    index = next((i for i, item in enumerate(current['research']['modules']) if item['id'] == folder.name), None)
                    if index is None:
                        current['research']['modules'].append(module)
                    else:
                        current['research']['modules'][index] = module
                assets.extend(images); hashes[relative] = digest; imported.append(relative)
            except Exception as error:
                raise ValueError(f'{relative}: {error}') from error
    if not imported:
        return {'imported': [], 'message': 'No new or changed Word documents found.'}
    written, saved = [], False
    try:
        for src, payload in assets:
            path = root / src.lstrip('/')
            if not path.exists():
                atomic_write(path, payload); written.append(path)
        validate(current, root)
        if dry_run:
            return {'imported': imported, 'message': 'Documents validated; no content was changed.'}
        result = store.save(current)
        saved = True
        atomic_write(manifest_path, json_bytes(hashes))
        return {'imported': imported, 'backup': result['backup'], 'message': f'Imported {len(imported)} Word document(s). Rebuild the preview to see the changes.'}
    except Exception:
        if not saved:
            for path in written:
                path.unlink(missing_ok=True)
        raise
    finally:
        if dry_run:
            for path in written:
                path.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--all', action='store_true', help='Import all new or changed documents (the default).')
    parser.add_argument('--only', help='Import just this project/research folder name.')
    parser.add_argument('--force', action='store_true', help='Reimport unchanged documents, overriding direct editor changes.')
    parser.add_argument('--dry-run', action='store_true', help='Validate without saving shared content.')
    args = parser.parse_args()
    try:
        result = import_folders(force=args.force, only=args.only, dry_run=args.dry_run)
    except Exception as error:
        parser.exit(1, f'Import failed: {error}\n')
    for path in result['imported']:
        print(path)
    print(result['message'])


if __name__ == '__main__':
    main()
