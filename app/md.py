from __future__ import annotations

from pathlib import Path
import re
import markdown as mdlib

MD_EXTENSIONS = [
    "fenced_code",
    "tables",
    "toc",
    "codehilite",
]

_IMG_SRC_RE = re.compile(r'(<img[^>]+src=")([^"]+)(")', re.IGNORECASE)
_A_HREF_RE = re.compile(r'(<a[^>]+href=")([^"]+)(")', re.IGNORECASE)

def _rewrite_relative_urls(html: str, asset_prefix: str | None) -> str:
    """
    If asset_prefix is provided, rewrite relative URLs like:
      images/foo.png  ->  {asset_prefix}images/foo.png
      files/handout.pdf -> {asset_prefix}files/handout.pdf

    Do NOT rewrite:
      - absolute URLs (http/https)
      - root URLs (/assets/..., /static/..., etc.)
      - fragment links (#toc)
      - mailto:
    """
    if not asset_prefix:
        return html

    def should_rewrite(url: str) -> bool:
        url = url.strip()
        if not url:
            return False
        if url.startswith(("http://", "https://", "/")):
            return False
        if url.startswith(("#", "mailto:")):
            return False
        return True

    def repl_img(m: re.Match) -> str:
        prefix, url, suffix = m.group(1), m.group(2), m.group(3)
        if should_rewrite(url):
            url = asset_prefix.rstrip("/") + "/" + url.lstrip("/")
        return prefix + url + suffix

    def repl_a(m: re.Match) -> str:
        prefix, url, suffix = m.group(1), m.group(2), m.group(3)
        if should_rewrite(url):
            url = asset_prefix.rstrip("/") + "/" + url.lstrip("/")
        return prefix + url + suffix

    html = _IMG_SRC_RE.sub(repl_img, html)
    html = _A_HREF_RE.sub(repl_a, html)
    return html


def render_markdown_file(path: Path, asset_prefix: str | None = None) -> tuple[str, dict]:
    """
    Returns: (html, meta)
    meta currently includes toc; hook remains for future front matter.
    asset_prefix example:
      /assets/cyber-for-beginners/day1/
    """
    text = path.read_text(encoding="utf-8")
    md = mdlib.Markdown(extensions=MD_EXTENSIONS)
    html = md.convert(text)
    html = _rewrite_relative_urls(html, asset_prefix=asset_prefix)
    return html, {"toc": md.toc}
