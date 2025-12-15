from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

import yaml
from flask import Blueprint, current_app, abort, render_template
from flask import send_from_directory

from .md import render_markdown_file


bp = Blueprint("workshops", __name__)


@dataclass
class NavPage:
    title: str
    file: str  # filename within day folder, e.g. "01-welcome-and-framing.md"


@dataclass
class NavDay:
    slug: str
    title: str
    pages: list[NavPage]


@dataclass
class NavWorkshop:
    slug: str
    title: str
    days: list[NavDay]


def content_root() -> Path:
    return Path(current_app.config["CONTENT_ROOT"]).resolve()


def load_nav() -> list[NavWorkshop]:
    nav_path = content_root() / "workshops.yml"
    if not nav_path.exists():
        return []

    raw = yaml.safe_load(nav_path.read_text(encoding="utf-8")) or {}
    workshops_raw = raw.get("workshops", [])

    workshops: list[NavWorkshop] = []
    for w in workshops_raw:
        days: list[NavDay] = []
        for d in w.get("days", []):
            pages = [NavPage(title=p["title"], file=p["file"]) for p in d.get("pages", [])]
            days.append(NavDay(slug=d["slug"], title=d["title"], pages=pages))
        workshops.append(NavWorkshop(slug=w["slug"], title=w["title"], days=days))
    return workshops


def find_workshop(nav: list[NavWorkshop], slug: str) -> Optional[NavWorkshop]:
    for w in nav:
        if w.slug == slug:
            return w
    return None


def flatten_pages(workshop: NavWorkshop) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for day in workshop.days:
        for p in day.pages:
            out.append({
                "day_slug": day.slug,
                "day_title": day.title,
                "file": p.file,
                "title": p.title,
                "url_slug": slugify_filename(p.file),
            })
    return out


def slugify_filename(filename: str) -> str:
    if filename.lower().endswith(".md"):
        return filename[:-3]
    return filename


def file_for_page(workshop_slug: str, day_slug: str, page_slug: str) -> Path:
    return content_root() / workshop_slug / day_slug / f"{page_slug}.md"


@bp.get("/")
def home():
    nav = load_nav()
    index_path = content_root() / "index.md"
    if not index_path.exists():
        html = "<h1>Workshop Site</h1><p>Add content/index.md</p>"
        return render_template("index.html", nav=nav, html=html, toc=None)

    html, meta = render_markdown_file(index_path, asset_prefix="/assets/")
    return render_template("index.html", nav=nav, html=html, toc=meta.get("toc"))


@bp.get("/workshops/<workshop_slug>/")
def workshop_landing(workshop_slug: str):
    nav = load_nav()
    workshop = find_workshop(nav, workshop_slug)
    if not workshop:
        abort(404)

    landing = content_root() / workshop_slug / "index.md"
    html = None
    toc = None
    if landing.exists():
        html, meta = render_markdown_file(landing, asset_prefix=f"/assets/{workshop_slug}/")
        toc = meta.get("toc")

    return render_template(
        "workshop.html",
        nav=nav,
        workshop=workshop,
        html=html,
        toc=toc,
    )


@bp.get("/workshops/<workshop_slug>/<day_slug>/")
def day_landing(workshop_slug: str, day_slug: str):
    nav = load_nav()
    workshop = find_workshop(nav, workshop_slug)
    if not workshop:
        abort(404)

    day = next((d for d in workshop.days if d.slug == day_slug), None)
    if not day:
        abort(404)

    landing = content_root() / workshop_slug / day_slug / "index.md"
    html = None
    toc = None
    if landing.exists():
        html, meta = render_markdown_file(landing, asset_prefix=f"/assets/{workshop_slug}/{day_slug}/")
        toc = meta.get("toc")

    return render_template(
        "page.html",
        nav=nav,
        workshop=workshop,
        day=day,
        page_title=day.title,
        html=html or "<p>No day index yet.</p>",
        toc=toc,
        prev_page=None,
        next_page=None,
        current_url=None,
    )


@bp.get("/workshops/<workshop_slug>/<day_slug>/<page_slug>/")
def workshop_page(workshop_slug: str, day_slug: str, page_slug: str):
    nav = load_nav()
    workshop = find_workshop(nav, workshop_slug)
    if not workshop:
        abort(404)

    day = next((d for d in workshop.days if d.slug == day_slug), None)
    if not day:
        abort(404)

    page_path = file_for_page(workshop_slug, day_slug, page_slug)
    if not page_path.exists():
        abort(404)

    html, meta = render_markdown_file(page_path, asset_prefix=f"/assets/{workshop_slug}/{day_slug}/")

    linear = flatten_pages(workshop)
    current_idx = next(
        (i for i, p in enumerate(linear) if p["day_slug"] == day_slug and p["url_slug"] == page_slug),
        None
    )

    prev_page = None
    next_page = None
    if current_idx is not None:
        if current_idx > 0:
            prev_page = linear[current_idx - 1]
        if current_idx < len(linear) - 1:
            next_page = linear[current_idx + 1]

    def build_url(p: dict[str, Any]) -> str:
        return f"/workshops/{workshop.slug}/{p['day_slug']}/{p['url_slug']}/"

    prev_payload = {"title": prev_page["title"], "url": build_url(prev_page)} if prev_page else None
    next_payload = {"title": next_page["title"], "url": build_url(next_page)} if next_page else None

    return render_template(
        "page.html",
        nav=nav,
        workshop=workshop,
        day=day,
        page_title=page_slug.replace("-", " "),
        html=html,
        toc=meta.get("toc"),
        prev_page=prev_payload,
        next_page=next_payload,
        current_url=f"/workshops/{workshop_slug}/{day_slug}/{page_slug}/",
    )


@bp.get("/assets/<path:asset_path>")
def assets(asset_path: str):
    """
    Serve static assets stored under the content directory.
    Example:
      /assets/cyber-for-beginners/day1/images/day1-welcome-framing.png
    """
    root = content_root()
    full_path = (root / asset_path).resolve()

    if not str(full_path).startswith(str(root)):
        abort(404)

    if not full_path.exists() or not full_path.is_file():
        abort(404)

    return send_from_directory(root, asset_path)
