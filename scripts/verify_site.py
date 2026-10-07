"""Check a local AcademicPages/Jekyll build for broken site links and sample content."""

from html.parser import HTMLParser
import json
from pathlib import Path
from urllib.parse import unquote, urlparse


ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "_site"
BASEURL = ""


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if attributes.get("id"):
            self.ids.add(attributes["id"])
        for key in ("href", "src"):
            if attributes.get(key):
                self.links.append(attributes[key])


def target_for(source: Path, raw: str) -> tuple[Path | None, str]:
    parsed = urlparse(raw)
    if raw.startswith("//") or (parsed.netloc and parsed.netloc != "fahome10bd.github.io"):
        return None, parsed.fragment
    if parsed.scheme and parsed.scheme not in ("http", "https"):
        return None, parsed.fragment
    path = unquote(parsed.path)
    if not path:
        return source, parsed.fragment
    if BASEURL:
        if path.startswith(BASEURL + "/") or path == BASEURL:
            path = path[len(BASEURL):]
        elif path.startswith("/"):
            # A root-relative path outside the project site's base URL would break on GitHub Pages.
            raise ValueError(f"Link omits {BASEURL}: {raw}")
    target = SITE / path.lstrip("/") if parsed.netloc or raw.startswith("/") else source.parent / path
    if target.is_dir() or path.endswith("/"):
        target /= "index.html"
    return target.resolve(), parsed.fragment


def main() -> None:
    if not (SITE / "index.html").exists():
        raise SystemExit("Build the site with Jekyll before running this verifier")
    pages = {}
    for file in SITE.rglob("*.html"):
        page = Page()
        page.feed(file.read_text(encoding="utf-8"))
        pages[file.resolve()] = page
    failures = []
    local_links = 0
    for source, page in pages.items():
        for raw in page.links:
            try:
                target, fragment = target_for(source, raw)
            except ValueError as error:
                failures.append(f"{source.relative_to(SITE)}: {error}")
                continue
            if target is None:
                continue
            if not target.exists():
                failures.append(f"{source.relative_to(SITE)} -> {raw} (missing {target})")
                continue
            local_links += 1
            if fragment and target.suffix == ".html":
                target_page = pages.get(target)
                if target_page is not None and fragment not in target_page.ids:
                    failures.append(f"{source.relative_to(SITE)} -> {raw} (missing anchor)")
    html_text = "\n".join(file.read_text(encoding="utf-8") for file in pages)
    for sample in ("Your Sidebar Name", "GitHub University", "Paper Title Number", "Red Brick University", "none@example.org"):
        if sample in html_text:
            failures.append(f"Upstream sample content remains: {sample}")
    if failures:
        raise AssertionError("\n".join(failures[:80]))
    projects = json.loads((ROOT / '_data/projects.json').read_text(encoding='utf-8'))
    documents = list((ROOT / '_portfolio').glob('*.md'))
    assert len(list((ROOT / "_publications").glob("*.md"))) == 1
    assert {file.stem for file in documents} == set(projects), 'Project data and collection files differ'
    for key, project in projects.items():
        output = SITE / 'portfolio' / key / 'index.html'
        assert output.exists(), f'Missing project page: {key}'
        assert project['title'].replace('&', '&amp;') in output.read_text(encoding='utf-8'), f'Missing project title: {key}'
    assert not (SITE / 'content').exists(), 'Word source folders must not be published'
    assert not (SITE / 'scripts').exists(), 'Local editor must not be published'
    print(f"Verified {len(pages)} generated HTML pages, {local_links} local links, one publication and {len(projects)} projects")


if __name__ == "__main__":
    main()
