# Shiwei Wang Homepage

This is a local static homepage ready for GitHub Pages.

## Maintenance Guide

See `docs/maintenance-and-update-guide.md` for the ongoing maintenance and update workflow.

## Publishing Guide

See `docs/github-pages-publishing-guide.md` for publishing this homepage with GitHub Pages.

## Update Content

- Edit `content/profile.md` for personal information, research interests, education, experience, awards, and service.
- Edit `content/publications.md` for publications, preprints, and presentations.
- Keep `CV.pdf` in the repository root if you want the CV link to keep working.

## Rebuild

Run:

```bash
python3 build.py
```

The script regenerates `index.html` from the Markdown files.

## Check

Run:

```bash
python3 -m unittest discover -s tests
```
