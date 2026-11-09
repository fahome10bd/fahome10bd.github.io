"""Sync Word documents from content/tracks/<track_folder>/<project_name>.docx into _data/projects.json."""
import json
from pathlib import Path
import docx

ROOT = Path(__file__).resolve().parent.parent
TRACKS_DIR = ROOT / 'content' / 'tracks'
PROJECTS_JSON = ROOT / '_data' / 'projects.json'

def parse_track_doc(doc_path: Path):
    doc = docx.Document(doc_path)
    metadata = {}
    blocks = []
    current_heading = None
    current_body_lines = []

    for p in doc.paragraphs:
        text = p.text.strip()
        if not text or text.startswith('―'):
            continue

        # Check for multiple metadata lines inside one paragraph
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        is_meta_para = False
        for line in lines:
            if ':' in line:
                first_colon = line.find(':')
                label = line[:first_colon].strip().lower()
                val = line[first_colon + 1:].strip()
                if label in ('title', 'summary', 'context', 'role', 'order', 'featured', 'track', 'slug/key', 'key'):
                    metadata[label] = val
                    is_meta_para = True

        if is_meta_para:
            continue

        # Check for heading
        is_heading = (
            p.style.name.startswith('Heading')
            or (p.runs and p.runs[0].bold and len(text) < 80 and not text.endswith('.'))
        )

        # Ignore the document title as a block heading if it matches metadata title
        if is_heading and metadata.get('title') and text.lower() == metadata['title'].lower():
            continue

        if is_heading:
            if current_heading and current_body_lines:
                blocks.append({
                    'type': 'text',
                    'heading': current_heading,
                    'body': '\n\n'.join(current_body_lines)
                })
                current_body_lines = []
            current_heading = text
        else:
            if current_heading:
                current_body_lines.append(text)

    if current_heading and current_body_lines:
        blocks.append({
            'type': 'text',
            'heading': current_heading,
            'body': '\n\n'.join(current_body_lines)
        })

    return metadata, blocks

def main():
    if not TRACKS_DIR.exists():
        print("No content/tracks directory found.")
        return

    projects = json.loads(PROJECTS_JSON.read_text(encoding='utf-8'))
    updated_count = 0

    for track_folder in sorted(TRACKS_DIR.iterdir()):
        if not track_folder.is_dir():
            continue
        for doc_file in sorted(track_folder.glob('*.docx')):
            try:
                meta, blocks = parse_track_doc(doc_file)
                key = meta.get('slug/key') or meta.get('key')
                if not key:
                    title = meta.get('title', '').strip().lower()
                    for k, v in projects.items():
                        if v.get('title', '').strip().lower() == title:
                            key = k
                            break

                if key and key in projects:
                    if meta.get('title'):
                        projects[key]['title'] = meta['title']
                    if meta.get('summary'):
                        projects[key]['summary'] = meta['summary']
                    if meta.get('context'):
                        projects[key]['context'] = meta['context']
                    if meta.get('role'):
                        projects[key]['role'] = meta['role']
                    if meta.get('order'):
                        try:
                            projects[key]['order'] = int(meta['order'])
                        except ValueError:
                            pass
                    if meta.get('featured'):
                        projects[key]['featured'] = meta['featured'].lower() in ('yes', 'true')
                    if blocks:
                        projects[key]['blocks'] = blocks
                    updated_count += 1
                    print(f"Synced {doc_file.name} -> {key} ({len(blocks)} sections)")
            except Exception as e:
                print(f"Error reading {doc_file.name}: {e}")

    PROJECTS_JSON.write_text(json.dumps(projects, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f"Sync complete. Updated {updated_count} projects in _data/projects.json.")

if __name__ == '__main__':
    main()
