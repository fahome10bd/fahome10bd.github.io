# Mohammad Mahmudul Hasan academic portfolio

This site uses AcademicPages and Jekyll for a professor-facing MSc/PhD research portfolio. It retains the academic sidebar, navigation, publication collection, and project pages, with consistent blue accents and readable typography.

## Main editing workflow

**Edit Word documents in `content/projects/` and `content/research/`, then import and rebuild.** Existing projects and research directions have populated documents. New-item templates are in `content/templates/`.

Read [the Word editing guide](content/README.md) for the folder structure, section headings, embedded pictures, captions, and import commands.

Start the optional local browser editor from this directory:

```powershell
python -m pip install -r scripts/requirements.txt
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/start_editor.ps1
```

Open **http://127.0.0.1:8765/**. Use **Import Word folders**, then **Save & rebuild preview**. The editor supports text blocks, image uploads with captions and descriptions, ordering, and adding/removing items. It binds only to your own computer and keeps backups before saves. Keep its terminal running; Ctrl+C stops it.

For a complete command-line import and build:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/import_and_preview.ps1 --all
```

The Word importer and browser editor use only the Python standard library. The downloadable CV renderer additionally uses ReportLab. Jekyll requires Ruby and Bundler; the build script uses the adjacent isolated `academicpages_runtime` when present and falls back to an installed Bundler otherwise.

## Content and formatting

| Content | Source |
| --- | --- |
| Name, profiles, employer, contact details | `_config.yml` |
| Navigation | `_data/navigation.yml` |
| Homepage | `_pages/about.md` |
| Research directions | `content/research/*/research.docx` → `_data/research.json` |
| Project case studies | `content/projects/*/project.docx` → `_data/projects.json` and generated `_portfolio/*.md` |
| Shared text/image formatting | `_includes/content-blocks.html` and `_sass/layout/_academic.scss` |
| Publication | `_publications/retinal-oct-explainable-ai.md` |
| Online CV and downloadable PDF content | `_data/cv.json` |
| PDF generation | `python scripts/build_cv.py` |

Research and Projects use the same block renderer. Word and the local editor feed the same JSON data; choose Word as the primary source for any item you maintain that way. A changed Word import replaces that item's direct editor changes. The online CV and PDF share one content file, including the publication's original author order.

## Validation

```powershell
python scripts/test_content_workflow.py -v
python scripts/verify_site.py
node --check scripts/editor/editor.js
```

The first command checks save backups, rollback, revision conflicts, image uploads, request boundaries, Word image extraction, invalid import batches, and repeatable imports. The site verifier checks generated links, anchors, project pages, sample content, and exclusion of local source/editor folders.

## Publishing

The repository is configured for **https://fahome10bd.github.io/** with an empty `baseurl`. Review local changes and push to `main` to trigger the usual GitHub Pages deployment. Check the live pages and CV after deployment. Local importing or rebuilding does not publish changes.

The AcademicPages theme retains its MIT [LICENSE](LICENSE) and attribution. Private application materials remain outside this site repository.
