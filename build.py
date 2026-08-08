from __future__ import annotations

import html
import re
from datetime import date
from pathlib import Path


SITE_TITLE = "Shiwei Wang"
DESCRIPTION = "Personal academic homepage of Shiwei Wang."
CONTENT_FILES = ("profile.md", "publications.md")


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "section"


def render_inline(text: str) -> str:
    rendered = html.escape(text, quote=True)
    rendered = re.sub(
        r"\[([^\]]+)\]\(((?:[^()]|\([^)]*\))+)\)",
        lambda match: f'<a href="{match.group(2)}">{match.group(1)}</a>',
        rendered,
    )
    rendered = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", rendered)
    return rendered


def markdown_to_html(markdown: str) -> str:
    blocks: list[str] = []
    paragraph: list[str] = []
    list_items: list[str] = []

    def flush_paragraph() -> None:
        if paragraph:
            text = " ".join(line.strip() for line in paragraph)
            blocks.append(f"<p>{render_inline(text)}</p>")
            paragraph.clear()

    def flush_list() -> None:
        if list_items:
            items = "\n".join(f"<li>{render_inline(item)}</li>" for item in list_items)
            blocks.append(f"<ul>\n{items}\n</ul>")
            list_items.clear()

    for raw_line in markdown.splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()

        if not stripped:
            flush_paragraph()
            flush_list()
            continue

        heading = re.match(r"^(#{1,3})\s+(.+)$", stripped)
        if heading:
            flush_paragraph()
            flush_list()
            level = len(heading.group(1))
            text = heading.group(2).strip()
            if level == 1:
                blocks.append(f"<h1>{render_inline(text)}</h1>")
            else:
                blocks.append(
                    f'<h{level} id="{slugify(text)}">{render_inline(text)}</h{level}>'
                )
            continue

        if stripped.startswith("- "):
            flush_paragraph()
            list_items.append(stripped[2:].strip())
            continue

        flush_list()
        paragraph.append(stripped)

    flush_paragraph()
    flush_list()
    return "\n".join(blocks)


def extract_sections(markdown: str) -> list[tuple[str, str]]:
    sections: list[tuple[str, str]] = []
    for line in markdown.splitlines():
        match = re.match(r"^##\s+(.+)$", line.strip())
        if match:
            title = match.group(1).strip()
            sections.append((title, slugify(title)))
    return sections


def render_page(content_html: str, nav_items: list[tuple[str, str]]) -> str:
    nav = "\n".join(
        f'<a href="#{section_id}">{html.escape(title)}</a>' for title, section_id in nav_items
    )
    year = date.today().year
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{html.escape(DESCRIPTION, quote=True)}">
  <title>{html.escape(SITE_TITLE)}</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <header class="site-header">
    <nav class="nav" aria-label="Primary navigation">
      {nav}
    </nav>
  </header>
  <main class="page">
    <article class="content">
      {content_html}
    </article>
  </main>
  <footer class="footer">
    <span>&copy; {year} Shiwei Wang.</span>
    <span>Built from Markdown for GitHub Pages.</span>
  </footer>
</body>
</html>
"""


def build_site(root: Path | None = None, output_path: Path | None = None) -> Path:
    root = Path.cwd() if root is None else root
    output_path = root / "index.html" if output_path is None else output_path
    content_dir = root / "content"

    markdown_parts = [
        (content_dir / filename).read_text(encoding="utf-8") for filename in CONTENT_FILES
    ]
    markdown = "\n\n".join(markdown_parts)
    html_body = markdown_to_html(markdown)
    nav_items = extract_sections(markdown)
    output_path.write_text(render_page(html_body, nav_items), encoding="utf-8")
    return output_path


if __name__ == "__main__":
    path = build_site()
    print(f"Generated {path}")
