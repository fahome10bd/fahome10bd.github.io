# Mohammad Mahmudul Hasan academic website

This repository uses the [AcademicPages](https://github.com/academicpages/academicpages.github.io) Jekyll template, adapted for Mohammad Mahmudul Hasan's graduate research applications. It preserves the AcademicPages theme, publication and portfolio collections, sidebar profile, navigation and Markdown CV structure. The theme is distributed under the included MIT [LICENSE](LICENSE).

The site is configured as a GitHub Pages **project site** for this repository, `fahome10bd/mahmudul`. After Pages is enabled, its expected address is **https://fahome10bd.github.io/mahmudul/**. The `_config.yml` settings use `url: https://fahome10bd.github.io` and `baseurl: /mahmudul`, matching [GitHub's Jekyll guidance for project sites](https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll/creating-a-github-pages-site-with-jekyll).

## What to edit

| Content | File or folder |
| --- | --- |
| Name, employer, GitHub, LinkedIn, email, site URL | `_config.yml` |
| Header links | `_data/navigation.yml` |
| Academic homepage | `_pages/about.md` |
| Research statement | `_pages/research.md` |
| Publication entry | `_publications/retinal-oct-explainable-ai.md` |
| Project case studies | `_portfolio/*.md` |
| Online CV | `_pages/cv.md` |
| Downloadable CV PDF | `files/Mohammad_Mahmudul_Hasan_Academic_CV.pdf` |

The paper appears once in the Publications collection. The original old site and its four field-specific draft CVs are retained outside this repository in `higher_studies_portfolio/`, rather than being presented as completed academic records here.

## Preview and publish

With Ruby and Bundler installed, run from the repository directory:

```powershell
bundle install
bundle exec jekyll serve --baseurl ""
```

Then preview `http://localhost:4000/`. A GitHub Pages build or local Jekyll build is required; opening Markdown source files or a previous `index.html` does not preview the theme.

To publish, push the reviewed repository to `main`, then set **Settings → Pages → Build and deployment → Source: Deploy from a branch → main → / (root)**. GitHub Pages builds the Jekyll site. The included GitHub Actions workflow separately checks that Jekyll can build on pushes and pull requests. No GitHub push or Pages settings change is performed by this local package.

If the repository is renamed to `fahome10bd.github.io` for a root-level user site, change `baseurl` to `""` and `repository` to `fahome10bd/fahome10bd.github.io` before publishing.

## Before sending the link to professors

- Add a current email if desired; no working address was provided, so the sidebar currently shows GitHub and LinkedIn instead.
- Confirm the team-lead promotion date and individual contribution to the OCT paper before adding those details.
- Add one evidence-backed result, method or shareable visual to each priority case study when available. No performance numbers have been invented.
- Confirm the current LinkedIn URL and ensure employer material can be described publicly.
- Check the live project-site links and downloadable PDF after GitHub Pages finishes building.

The seven project summaries and four research areas describe completed experience and proposed research separately. Vision-language/LLM research is described as an intended direction.
