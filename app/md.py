from __future__ import annotations

from pathlib import Path
import markdown as mdlib

MD_EXTENSIONS = [
    "fenced_code",
    "tables",
    "toc",
    "codehilite",  # basic code highlighting
]

def render_markdown_file(path: Path) -> tuple[str, dict]:
    """
    Returns: (html, meta)
    meta is currently minimal; we keep this hook for future (front matter, etc).
    """
    text = path.read_text(encoding="utf-8")
    md = mdlib.Markdown(extensions=MD_EXTENSIONS)
    html = md.convert(text)
    return html, {"toc": md.toc}
