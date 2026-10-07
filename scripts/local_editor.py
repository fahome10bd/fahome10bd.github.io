"""Loopback-only editor for Research and Projects. Python standard library only."""

import argparse
import hashlib
import json
import mimetypes
import os
import re
import secrets
import subprocess
import sys
import threading
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parent.parent
MAX_JSON = 2 * 1024 * 1024
MAX_IMAGE = 15 * 1024 * 1024
SLUG = re.compile(r'[a-z0-9][a-z0-9-]{0,79}\Z')
IMAGE_PATH = re.compile(r'/(?:assets/images|images)/[A-Za-z0-9_./-]+\Z')


class Conflict(ValueError):
    pass


def json_bytes(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8')


def string(value, label, maximum=1000, required=False):
    if not isinstance(value, str) or len(value) > maximum or (required and not value.strip()):
        raise ValueError(f'{label} must be {"non-empty " if required else ""}text of at most {maximum} characters.')


def validate_blocks(blocks, root):
    if not isinstance(blocks, list) or len(blocks) > 100:
        raise ValueError('Each item can have up to 100 blocks.')
    for block in blocks:
        if not isinstance(block, dict):
            raise ValueError('Invalid content block.')
        if block.get('type') == 'text':
            string(block.get('heading'), 'Block heading', 200)
            string(block.get('body'), 'Block text', 100000)
            if not block.get('heading', '').strip() and not block.get('body', '').strip():
                raise ValueError('A text block needs a heading or body text.')
        elif block.get('type') == 'image':
            src = block.get('src', '')
            if not isinstance(src, str) or not IMAGE_PATH.fullmatch(src):
                raise ValueError('Upload an image or enter a local /images/ or /assets/images/ path.')
            image = (root / src.lstrip('/')).resolve()
            if not image.is_relative_to(root.resolve()) or image.suffix.lower() not in ('.png', '.jpg', '.jpeg', '.webp', '.gif') or not image.is_file():
                raise ValueError('The image must exist inside this site and use PNG, JPEG, WebP, or GIF.')
            string(block.get('alt'), 'Image description', 2000, required=True)
            string(block.get('caption'), 'Image caption', 2000)
            if block.get('size') not in ('full', 'medium'):
                raise ValueError('Choose full width or medium width for the image.')
        else:
            raise ValueError('Supported block types are text and image.')


def validate(content, root):
    if not isinstance(content, dict):
        raise ValueError('Invalid content payload.')
    projects, research = content.get('projects'), content.get('research')
    if not isinstance(projects, dict) or not 1 <= len(projects) <= 100:
        raise ValueError('Keep between 1 and 100 projects.')
    if not isinstance(research, dict):
        raise ValueError('Invalid research content.')
    string(research.get('introduction'), 'Research introduction', 100000, required=True)
    modules = research.get('modules')
    if not isinstance(modules, list) or not 1 <= len(modules) <= 100:
        raise ValueError('Keep between 1 and 100 research directions.')
    anchors = set()
    for module in modules:
        if not isinstance(module, dict) or not isinstance(module.get('id'), str) or not SLUG.fullmatch(module['id']) or module['id'] in anchors:
            raise ValueError('Research anchors must be unique lowercase names containing letters, numbers, and hyphens.')
        anchors.add(module['id'])
        string(module.get('title'), 'Research title', 200, required=True)
        string(module.get('summary'), 'Research summary', 1500)
        validate_blocks(module.get('blocks'), root)
    for key, project in projects.items():
        if not SLUG.fullmatch(key) or not isinstance(project, dict):
            raise ValueError('Project URL names can contain lowercase letters, numbers, and hyphens.')
        string(project.get('title'), 'Project title', 200, required=True)
        string(project.get('summary'), 'Project summary', 1500, required=True)
        string(project.get('context'), 'Project context', 200)
        string(project.get('role'), 'Your role', 200)
        if type(project.get('order')) is not int or not 1 <= project['order'] <= 1000:
            raise ValueError('Project order must be a whole number between 1 and 1000.')
        if type(project.get('featured')) is not bool:
            raise ValueError('Featured must be true or false.')
        anchor = project.get('research_anchor')
        if not isinstance(anchor, str) or (anchor and anchor not in anchors):
            raise ValueError(f'{project["title"]}: select an existing related research direction, or leave it blank.')
        validate_blocks(project.get('blocks'), root)


def project_document(key, project):
    return ('\n'.join([
        '---', 'layout: project', 'collection: portfolio',
        'title: ' + json.dumps(project['title'], ensure_ascii=False),
        'order: ' + str(project['order']), 'permalink: /portfolio/' + key + '/',
        'excerpt: ' + json.dumps(project['summary'], ensure_ascii=False),
        'content_key: ' + key, 'share: false', 'comments: false', '---', '',
    ])).encode('utf-8')


def atomic_write(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + '.' + secrets.token_hex(6) + '.tmp')
    try:
        temp.write_bytes(payload)
        os.replace(temp, path)
    finally:
        temp.unlink(missing_ok=True)


class ContentStore:
    def __init__(self, root):
        self.root = Path(root).resolve()
        self.lock = threading.RLock()

    def read(self):
        with self.lock:
            result = {'revisions': {}}
            for kind in ('projects', 'research'):
                raw = (self.root / '_data' / (kind + '.json')).read_bytes()
                result[kind] = json.loads(raw)
                result['revisions'][kind] = hashlib.sha256(raw).hexdigest()
            return result

    def save(self, content):
        with self.lock:
            if not isinstance(content, dict):
                raise ValueError('Invalid content payload.')
            previous = self.read()
            if content.get('revisions') != previous['revisions']:
                raise Conflict('The source files changed since this editor loaded. Reload the editor before saving.')
            validate(content, self.root)
            changes = {self.root / '_data' / (kind + '.json'): json_bytes(content[kind]) for kind in ('projects', 'research')}
            for key, project in content['projects'].items():
                changes[self.root / '_portfolio' / (key + '.md')] = project_document(key, project)
            for key in previous['projects'].keys() - content['projects'].keys():
                changes[self.root / '_portfolio' / (key + '.md')] = None
            originals = {path: path.read_bytes() if path.exists() else None for path in changes}
            stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
            backup = self.root / 'local' / 'editor-history' / stamp
            for path, raw in originals.items():
                if raw is not None:
                    target = backup / path.relative_to(self.root)
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(raw)
            try:
                for path, raw in changes.items():
                    if raw is None:
                        path.unlink(missing_ok=True)
                    else:
                        atomic_write(path, raw)
            except Exception:
                for path, raw in originals.items():
                    if raw is None:
                        path.unlink(missing_ok=True)
                    else:
                        atomic_write(path, raw)
                raise
            result = self.read()
            result['backup'] = str(backup.relative_to(self.root))
            return result

    def upload(self, payload, filename):
        if payload.startswith(b'\x89PNG\r\n\x1a\n'):
            suffix = '.png'
        elif payload.startswith(b'\xff\xd8\xff'):
            suffix = '.jpg'
        elif payload[:6] in (b'GIF87a', b'GIF89a'):
            suffix = '.gif'
        elif payload[:4] == b'RIFF' and payload[8:12] == b'WEBP':
            suffix = '.webp'
        else:
            raise ValueError('Please upload a PNG, JPEG, WebP, or GIF image.')
        stem = re.sub(r'[^a-z0-9-]+', '-', Path(filename).stem.lower()).strip('-')[:50] or 'image'
        relative = Path('assets/images/uploads') / (stem + '-' + secrets.token_hex(6) + suffix)
        atomic_write(self.root / relative, payload)
        return '/' + relative.as_posix()


class EditorServer(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(self, root=ROOT, port=8765):
        self.store = ContentStore(root)
        self.token = secrets.token_urlsafe(32)
        self.job_lock = threading.Lock()
        self.job = {'state': 'idle', 'log': ''}
        super().__init__(('127.0.0.1', port), Handler)

    def rebuild(self):
        with self.job_lock:
            if self.job['state'] == 'running':
                raise Conflict('A preview build is already running.')
            self.job = {'state': 'running', 'log': ''}
        threading.Thread(target=self._build, daemon=True).start()

    def _build(self):
        root = self.store.root
        commands = [[sys.executable, 'scripts/build_cv.py']]
        if os.name == 'nt':
            commands.append(['powershell.exe', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', 'scripts/build_site.ps1'])
        else:
            commands.append(['bundle', 'exec', 'jekyll', 'build', '--strict_front_matter'])
        commands.append([sys.executable, 'scripts/verify_site.py'])
        logs = []
        try:
            for command in commands:
                process = subprocess.run(command, cwd=root, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='replace', timeout=180, creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
                logs.append(process.stdout)
                if process.returncode:
                    raise RuntimeError(f'Build step failed (exit {process.returncode}).')
            state = 'complete'
        except Exception as error:
            logs.append(str(error))
            state = 'failed'
        with self.job_lock:
            self.job = {'state': state, 'log': '\n'.join(logs)[-20000:]}


class Handler(BaseHTTPRequestHandler):
    def reply(self, status, payload, content_type='application/json; charset=utf-8'):
        if isinstance(payload, dict):
            payload = json_bytes(payload)
        elif isinstance(payload, str):
            payload = payload.encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(payload)))
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('X-Frame-Options', 'SAMEORIGIN')
        self.end_headers()
        self.wfile.write(payload)

    def allowed(self, mutation=False):
        port = self.server.server_address[1]
        allowed_hosts = {f'127.0.0.1:{port}', f'localhost:{port}'}
        if self.headers.get('Host') not in allowed_hosts:
            self.reply(403, {'error': 'Use the local editor address shown in the terminal.'})
            return False
        origin = self.headers.get('Origin')
        if origin and origin not in {f'http://{host}' for host in allowed_hosts}:
            self.reply(403, {'error': 'Cross-origin requests are not allowed.'})
            return False
        if mutation and not secrets.compare_digest(self.headers.get('X-Editor-Token', ''), self.server.token):
            self.reply(403, {'error': 'Reload the local editor to continue.'})
            return False
        return True

    def body(self, maximum):
        try:
            size = int(self.headers.get('Content-Length', '0'))
        except ValueError:
            raise ValueError('Invalid request size.')
        if not 0 < size <= maximum:
            raise ValueError(f'The request must be between 1 byte and {maximum // 1024 // 1024} MB.')
        raw = self.rfile.read(size)
        if len(raw) != size:
            raise ValueError('Incomplete request.')
        return raw

    def file(self, base, relative, preview=False):
        base = base.resolve()
        path = (base / unquote(relative)).resolve()
        if not path.is_relative_to(base):
            self.reply(403, {'error': 'Invalid file path.'})
            return
        if path.is_dir():
            path /= 'index.html'
        if not path.is_file():
            self.reply(404, {'error': 'File not found. Rebuild the preview if needed.'})
            return
        raw = path.read_bytes()
        mime = mimetypes.guess_type(path.name)[0] or 'application/octet-stream'
        if preview and path.suffix == '.html':
            html = raw.decode('utf-8')
            # Keep navigation on the local preview, including original absolute theme links.
            html = re.sub(r'(href|src)="https://fahome10bd\.github\.io/?', r'\1="/preview/', html)
            html = re.sub(r'(href|src)="/(?!preview/|/)', r'\1="/preview/', html)
            raw = html.encode('utf-8')
        self.reply(200, raw, mime + ('; charset=utf-8' if mime in ('text/html', 'text/css', 'text/javascript') else ''))

    def do_GET(self):
        if not self.allowed():
            return
        path = urlparse(self.path).path
        try:
            if path == '/api/content':
                result = self.server.store.read()
                result['token'] = self.server.token
                self.reply(200, result)
            elif path == '/api/build':
                with self.server.job_lock:
                    self.reply(200, self.server.job.copy())
            elif path in ('/', '/index.html'):
                self.file(self.server.store.root / 'scripts/editor', 'index.html')
            elif path.startswith('/editor/'):
                self.file(self.server.store.root / 'scripts/editor', path[len('/editor/'):])
            elif path.startswith('/preview/'):
                self.file(self.server.store.root / '_site', path[len('/preview/'):], preview=True)
            elif path.startswith('/assets/images/') or path.startswith('/images/'):
                base = 'assets/images' if path.startswith('/assets/images/') else 'images'
                self.file(self.server.store.root / base, path[len('/' + base + '/'):])
            else:
                self.reply(404, {'error': 'Not found.'})
        except Exception as error:
            self.reply(500, {'error': str(error)})

    def do_PUT(self):
        if not self.allowed(mutation=True):
            return
        if urlparse(self.path).path != '/api/content':
            self.reply(404, {'error': 'Not found.'})
            return
        try:
            with self.server.store.lock, self.server.job_lock:
                if self.server.job['state'] == 'running':
                    raise Conflict('Wait for the preview build to finish before saving.')
                self.reply(200, self.server.store.save(json.loads(self.body(MAX_JSON))))
        except Conflict as error:
            self.reply(409, {'error': str(error)})
        except (ValueError, KeyError, TypeError) as error:
            self.reply(400, {'error': str(error)})
        except Exception as error:
            self.reply(500, {'error': str(error)})

    def do_POST(self):
        if not self.allowed(mutation=True):
            return
        try:
            path = urlparse(self.path).path
            if path == '/api/upload':
                src = self.server.store.upload(self.body(MAX_IMAGE), unquote(self.headers.get('X-Filename', 'image')))
                self.reply(201, {'src': src})
            elif path == '/api/import':
                from import_documents import import_folders
                request = json.loads(self.body(MAX_JSON))
                if not isinstance(request, dict):
                    raise ValueError('Invalid import request.')
                with self.server.store.lock, self.server.job_lock:
                    if self.server.job['state'] == 'running':
                        raise Conflict('Wait for the preview build to finish before importing.')
                    if request.get('revisions') != self.server.store.read()['revisions']:
                        raise Conflict('The content changed. Reload the editor before importing.')
                    result = import_folders(self.server.store.root)
                    result['content'] = self.server.store.read()
                    self.reply(200, result)
            elif path == '/api/build':
                with self.server.store.lock:
                    self.server.rebuild()
                self.reply(202, {'state': 'running'})
            else:
                self.reply(404, {'error': 'Not found.'})
        except Conflict as error:
            self.reply(409, {'error': str(error)})
        except (ValueError, TypeError, KeyError) as error:
            self.reply(400, {'error': str(error)})
        except Exception as error:
            self.reply(500, {'error': str(error)})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=8765)
    args = parser.parse_args()
    server = EditorServer(port=args.port)
    print(f'Local portfolio editor: http://127.0.0.1:{server.server_address[1]}/', flush=True)
    print('Press Ctrl+C to stop. Saves stay in this repository; publishing is a separate step.', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == '__main__':
    main()
