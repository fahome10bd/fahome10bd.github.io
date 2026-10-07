# Editing your portfolio in Word

Use the Word files in this folder as your main authoring workflow. The importer turns their sections and pictures into the website's shared content blocks. Website fonts, spacing, and image widths are controlled by the theme, so you do not need to reproduce the website layout in Word.

## Edit an existing project

Open `projects/<project-name>/project.docx`, edit its text, and save it in the same folder. Existing project and research documents are already populated with the current site content.

The labelled fields at the top control the page:

| Field | Purpose |
| --- | --- |
| Title | Website page title; edit this field even if you also change the large Word title |
| Summary | Introduction and project-list description |
| Context | Employer, institution, or project setting |
| Role | Your individual contribution |
| Order | Display position, from 1 to 1000 |
| Featured | `yes` or `no`; the first three featured projects appear on the homepage |
| Related research | Optional research folder name linking to its section |

Use **Heading 1** for each content section, such as Problem, My contribution, Method, Evaluation, or Limitations. Any section names are accepted. Ordinary paragraphs, bold and italic text, links, bullet/numbered lists, and simple tables become website text. The first table row is treated as its header; avoid merged cells.

## Add pictures

1. In Word, use **Insert → Pictures** and choose **In Line with Text**.
2. Put the picture beneath the section where it belongs.
3. Add these ordinary paragraphs immediately below it:

```text
Caption: What this figure shows and why it matters.
Alt: A short description of the information visible in the figure.
Image width: full
```

`Image width` accepts `full` or `medium`. A Word Caption-style paragraph also works as a caption, and Word's picture Alt Text can supply the description. Every image needs an Alt description. Pictures are extracted automatically; there is no need to maintain a separate images folder. Use PNG, JPEG, WebP, or GIF pictures up to 15 MB each. Keep captions beside the relevant image and put images outside tables. Convert charts and shapes to pictures before inserting them.

## Add a new project

Create a folder such as `projects/urban-reconstruction/`. Copy `templates/project-template.docx` into it and rename the copy **project.docx**. Fill the metadata and replace every `[REPLACE ...]` instruction. Use a lowercase folder name with letters, numbers, and hyphens. That name becomes the permanent URL, for example `/portfolio/urban-reconstruction/`; changing the folder name creates a different item.

## Edit research

Use `research/<direction-name>/research.docx`. Research documents use Title and Summary fields and the same section/image rules. Copy `templates/research-template.docx` into a new research folder and name it **research.docx** to add a direction. Edit the research page's shared introduction or direction ordering in the local editor.

## Import and review

From the `mahmudul` directory:

```powershell
python -m pip install -r scripts/requirements.txt
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/start_editor.ps1
```

Open **http://127.0.0.1:8765/**. After saving your Word documents, click **Import Word folders**, then **Save & rebuild preview**. Open the site preview to see the real Jekyll pages. The editor also supports quick text edits, image uploads, new items, and block ordering.

If you prefer a command:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/import_and_preview.ps1 --all
```

Then use the local editor's preview at **http://127.0.0.1:8765/preview/**. Keep the editor terminal running while using it. Press Ctrl+C to stop it.

## How updates are handled

- Only new or changed Word files are imported. Unchanged files are skipped.
- Importing a changed Word file replaces that item's website content. For a given item, use Word as the main source; quick browser edits persist until its Word source is changed and imported again.
- All documents in a batch are checked before content is saved. Previous JSON data and project pages are backed up in `local/editor-history/` before a save.
- Removing a source document does not remove its website page. Use the editor's Remove action to intentionally remove a page, and move its Word source out of the import folder if you do not want it recreated later.
- Use `python scripts/import_documents.py --only urban-reconstruction` for one folder, `--dry-run` to validate, or `--force` to deliberately reimport unchanged Word files.
- The source Word folders, local editor, and backups are excluded from the published site. Imported images and the resulting public text are included.
- Imports and preview builds stay local. Publish by reviewing and pushing the repository through your normal GitHub workflow.

Use **.docx**, rather than the older binary **.doc** format. For a `.doc` source, open it in Word and Save As a `.docx` file first. Accept or reject tracked changes before importing.

## Recover a previous version

Choose a timestamped folder inside `local/editor-history/`. It contains the previous `_data/projects.json`, `_data/research.json`, and `_portfolio/*.md` files. Restore those files to the matching repository paths and rebuild. Keep the restored Word source consistent with the restored website content before the next import.
