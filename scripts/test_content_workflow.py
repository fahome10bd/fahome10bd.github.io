"""Regression checks for local content editing and Word import, using isolated folders."""
import copy
import http.client
import json
import shutil
import tempfile
import threading
import unittest
from pathlib import Path
from unittest.mock import patch
from zipfile import ZipFile

import local_editor
from import_documents import import_folders, parse_document
from local_editor import ContentStore, EditorServer, ROOT, validate

PNG = bytes.fromhex('89504e470d0a1a0a0000000d49484452000000010000000108060000001f15c4890000000b49444154789c636000020000050001a5f645400000000049454e44ae426082')


def fixture_doc(path, title='New project', bad=False):
    path.parent.mkdir(parents=True, exist_ok=True)
    media = '../outside.png' if bad else 'media/example.png'
    body = '''<w:p><w:r><w:t>Title: TITLE</w:t></w:r></w:p>
    <w:p><w:r><w:t>Summary: A reproducible case study.</w:t></w:r></w:p>
    <w:p><w:r><w:t>Order: 8</w:t></w:r></w:p>
    <w:p><w:r><w:t>Featured: no</w:t></w:r></w:p>
    <w:p><w:pPr><w:pStyle w:val="Heading1"/></w:pPr><w:r><w:t>Method</w:t></w:r></w:p>
    <w:p><w:r><w:rPr><w:b/></w:rPr><w:t>Important method</w:t></w:r></w:p>
    <w:p><w:pPr><w:pStyle w:val="ListBullet"/></w:pPr><w:r><w:t>First point</w:t></w:r></w:p>
    <w:p><w:hyperlink r:id="link"><w:r><w:t>Source</w:t></w:r></w:hyperlink></w:p>
    <w:p><w:r><w:drawing><wp:inline><wp:docPr id="1" name="Picture" descr="A project diagram"/><a:blip r:embed="image"/></wp:inline></w:drawing></w:r></w:p>
    <w:p><w:r><w:t>Caption: Diagram caption</w:t></w:r></w:p>
    <w:p><w:r><w:t>Image width: medium</w:t></w:r></w:p>
    <w:p><w:r><w:t>Text following the figure.</w:t></w:r></w:p>'''.replace('TITLE', title)
    with ZipFile(path, 'w') as archive:
        archive.writestr('word/document.xml', '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"><w:body>' + body + '</w:body></w:document>')
        archive.writestr('word/_rels/document.xml.rels', '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="image" Target="' + media + '"/><Relationship Id="link" Target="https://example.org/paper" TargetMode="External"/></Relationships>')
        archive.writestr('word/media/example.png', PNG)


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        shutil.copytree(ROOT / '_data', self.root / '_data')
        shutil.copytree(ROOT / '_portfolio', self.root / '_portfolio')
        self.store = ContentStore(self.root)

    def tearDown(self):
        self.temp.cleanup()

    def new_project(self):
        value = self.store.read()
        value['projects']['new-project'] = copy.deepcopy(next(iter(value['projects'].values())))
        value['projects']['new-project']['title'] = 'New project'
        value['projects']['new-project']['order'] = 8
        return value

    def test_save_creates_project_and_recoverable_backup(self):
        value = self.new_project()
        result = self.store.save(value)
        self.assertIn('new-project', self.store.read()['projects'])
        self.assertIn('permalink: /portfolio/new-project/', (self.root / '_portfolio/new-project.md').read_text())
        self.assertTrue((self.root / result['backup'] / '_data/projects.json').exists())

    def test_stale_revision_cannot_overwrite_new_content(self):
        old = self.store.read()
        self.store.save(self.new_project())
        with self.assertRaises(local_editor.Conflict):
            self.store.save(old)
        self.assertIn('new-project', self.store.read()['projects'])

    def test_invalid_image_path_cannot_escape_site(self):
        value = self.new_project()
        value['projects']['new-project']['blocks'].append({'type': 'image', 'src': '/images/../../private.png', 'alt': 'Description', 'caption': '', 'size': 'full'})
        before = self.store.read()
        with self.assertRaises(ValueError):
            self.store.save(value)
        self.assertEqual(before, self.store.read())

    def test_failed_save_rolls_back_all_source_files(self):
        before = self.store.read()
        writer = local_editor.atomic_write
        calls = 0
        def fail_once(path, payload):
            nonlocal calls
            calls += 1
            if calls == 3:
                raise OSError('Injected write failure')
            return writer(path, payload)
        with patch.object(local_editor, 'atomic_write', fail_once):
            with self.assertRaises(OSError):
                self.store.save(self.new_project())
        self.assertEqual(before, self.store.read())
        self.assertFalse((self.root / '_portfolio/new-project.md').exists())

    def test_word_import_preserves_text_image_order_and_is_repeatable(self):
        fixture_doc(self.root / 'content/projects/new-project/project.docx')
        result = import_folders(self.root)
        self.assertEqual(len(result['imported']), 1)
        project = self.store.read()['projects']['new-project']
        self.assertEqual([block['type'] for block in project['blocks']], ['text', 'image', 'text'])
        self.assertIn('**Important method**', project['blocks'][0]['body'])
        self.assertIn('- First point', project['blocks'][0]['body'])
        self.assertIn('[Source](https://example.org/paper)', project['blocks'][0]['body'])
        self.assertEqual(project['blocks'][1]['caption'], 'Diagram caption')
        self.assertEqual(project['blocks'][1]['size'], 'medium')
        self.assertEqual(project['blocks'][1]['alt'], 'A project diagram')
        self.assertEqual((self.root / project['blocks'][1]['src'].lstrip('/')).read_bytes(), PNG)
        self.assertEqual(import_folders(self.root)['imported'], [])
        src = project['blocks'][1]['src']
        import_folders(self.root, force=True)
        self.assertEqual(self.store.read()['projects']['new-project']['blocks'][1]['src'], src)

    def test_dry_run_leaves_no_content_or_extracted_images(self):
        fixture_doc(self.root / 'content/projects/new-project/project.docx')
        before = self.store.read()
        import_folders(self.root, dry_run=True)
        self.assertEqual(before, self.store.read())
        self.assertFalse((self.root / 'local/document-imports.json').exists())
        self.assertEqual(list(self.root.rglob('*.png')), [])

    def test_invalid_document_batch_does_not_partially_import(self):
        fixture_doc(self.root / 'content/projects/a-valid/project.docx')
        fixture_doc(self.root / 'content/projects/z-invalid/project.docx', bad=True)
        before = self.store.read()
        with self.assertRaises(ValueError):
            import_folders(self.root)
        self.assertEqual(before, self.store.read())
        self.assertFalse((self.root / 'local/document-imports.json').exists())

    def test_legacy_doc_reports_conversion_step(self):
        folder = self.root / 'content/projects/new-project'
        folder.mkdir(parents=True)
        (folder / 'project.doc').write_bytes(b'legacy document')
        with self.assertRaisesRegex(ValueError, 'Save the .doc file as project.docx'):
            import_folders(self.root)

    def test_word_numbering_and_simple_table_are_preserved(self):
        path = self.root / 'numbered.docx'
        fixture_doc(path)
        with ZipFile(path) as original:
            members = {name: original.read(name) for name in original.namelist()}
        members['word/document.xml'] = members['word/document.xml'].replace(b'<w:pStyle w:val="ListBullet"/>', b'<w:numPr><w:ilvl w:val="0"/><w:numId w:val="4"/></w:numPr>')
        members['word/numbering.xml'] = b'<w:numbering xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:abstractNum w:abstractNumId="2"><w:lvl w:ilvl="0"><w:numFmt w:val="decimal"/></w:lvl></w:abstractNum><w:num w:numId="4"><w:abstractNumId w:val="2"/></w:num></w:numbering>'
        table = b'<w:tbl><w:tr><w:tc><w:p><w:r><w:t>Metric</w:t></w:r></w:p></w:tc><w:tc><w:p><w:r><w:t>Value</w:t></w:r></w:p></w:tc></w:tr><w:tr><w:tc><w:p><w:r><w:t>Example</w:t></w:r></w:p></w:tc><w:tc><w:p><w:r><w:t>1</w:t></w:r></w:p></w:tc></w:tr></w:tbl>'
        members['word/document.xml'] = members['word/document.xml'].replace(b'</w:body>', table + b'</w:body>')
        with ZipFile(path, 'w') as changed:
            for name, raw in members.items():
                changed.writestr(name, raw)
        _, blocks, _ = parse_document(path)
        self.assertIn('1. First point', blocks[0]['body'])
        self.assertIn('| Metric | Value |', blocks[-1]['body'])
        self.assertIn('| --- | --- |', blocks[-1]['body'])

    def test_template_placeholders_cannot_be_imported(self):
        fixture_doc(self.root / 'content/projects/new-project/project.docx', title='[REPLACE with title]')
        with self.assertRaisesRegex(ValueError, 'Replace all template placeholders'):
            import_folders(self.root)

    def test_heading_only_block_is_valid_for_image_sections(self):
        value = self.new_project()
        value['projects']['new-project']['blocks'] = [{'type': 'text', 'heading': 'Results', 'body': ''}]
        validate(value, self.root)

    def test_http_upload_save_and_request_boundaries(self):
        preview = self.root / '_site'
        preview.mkdir()
        (preview / 'index.html').write_text('<a href="https://fahome10bd.github.io/research/">Research</a><img src="/images/figure.png">', encoding='utf-8')
        server = EditorServer(self.root, port=0)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        connection = http.client.HTTPConnection('127.0.0.1', server.server_address[1])
        def request(method, path, body=None, headers=None):
            connection.request(method, path, body=body, headers=headers or {})
            response = connection.getresponse()
            return response.status, response.read()
        try:
            status, raw = request('GET', '/api/content')
            self.assertEqual(status, 200)
            content = json.loads(raw)
            token = content.pop('token')
            self.assertEqual(request('GET', '/api/import')[0], 404)
            self.assertEqual(request('POST', '/api/import', '{}')[0], 403)
            self.assertEqual(request('POST', '/api/import', json.dumps({'revisions': content['revisions']}), {'X-Editor-Token': token})[0], 200)
            self.assertEqual(request('PUT', '/api/content', '[]', {'X-Editor-Token': token})[0], 400)
            self.assertEqual(request('PUT', '/api/content', json.dumps(content))[0], 403)
            self.assertEqual(request('POST', '/api/upload', PNG, {'X-Editor-Token': token, 'Origin': 'https://foreign.example'})[0], 403)
            self.assertEqual(request('GET', '/api/content', headers={'Host': 'foreign.example'})[0], 403)
            self.assertEqual(request('GET', '/preview/%2e%2e/_data/projects.json')[0], 403)
            self.assertEqual(request('POST', '/api/upload', b'not an image', {'X-Editor-Token': token})[0], 400)
            status, raw = request('POST', '/api/upload', PNG, {'X-Editor-Token': token, 'X-Filename': '../../figure.png'})
            self.assertEqual(status, 201)
            src = json.loads(raw)['src']
            self.assertTrue(src.startswith('/assets/images/uploads/figure-'))
            self.assertEqual(request('GET', src)[1], PNG)
            project = next(iter(content['projects'].values()))
            project['blocks'].append({'type': 'image', 'src': src, 'alt': 'Diagram', 'caption': 'Result', 'size': 'full'})
            self.assertEqual(request('PUT', '/api/content', json.dumps(content), {'X-Editor-Token': token})[0], 200)
            self.assertEqual(request('PUT', '/api/content', json.dumps(content), {'X-Editor-Token': token})[0], 409)
            status, raw = request('GET', '/preview/')
            self.assertEqual(status, 200)
            self.assertIn(b'href="/preview/research/"', raw)
            self.assertIn(b'src="/preview/images/figure.png"', raw)
        finally:
            connection.close(); server.shutdown(); server.server_close(); thread.join()


if __name__ == '__main__':
    unittest.main()
