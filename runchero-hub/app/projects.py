"""The allowlisted community projects shown on the hub.

Only the projects in this list are linked. Anything matching an excluded
token is dropped even if it is accidentally added later.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from urllib.parse import urlsplit

from . import config


@dataclass(frozen=True)
class Project:
    slug: str
    name: str
    tagline: str
    description: str
    port: int
    icon: str
    screenshot: str
    tags: tuple[str, ...] = field(default_factory=tuple)
    path: str = "/"
    note: str = ""
    internal: bool = False


PROJECTS: list[Project] = [
    Project(
        slug="info-depo",
        name="Runchero Information Depo",
        tagline="A sourced field library, available offline.",
        description=(
            "A sourced field library for the small farm: 1,598 public-domain books, "
            "plain-language fixes, formulas, equipment manuals, conversions, and "
            "topic depots. Everything works without an internet connection."
        ),
        port=8080,
        icon="depot.png",
        screenshot="info-depo.png",
        tags=("Library", "Offline", "Reference"),
    ),
    Project(
        slug="shop",
        name="Runchero Beef",
        tagline="Locally grown beef, cut for your table.",
        description=(
            "The co-op storefront for Runchero Beef: freezer shares, cuts by the "
            "pound, curated packages, published market-price checks, pickup and "
            "delivery. The demo cart never charges a card."
        ),
        port=8081,
        icon="cow.png",
        screenshot="shop.png",
        tags=("Shop", "Food", "Co-op"),
    ),
    Project(
        slug="map",
        name="Runchero Property Map",
        tagline="The farm, building by building.",
        description=(
            "An interactive pixel-art map of the property: buildings, fields, ponds, "
            "photos, construction notes, maintenance logs, and events. Built as an "
            "internal planning tool for the farm."
        ),
        port=8082,
        icon="tree.png",
        screenshot="map.png",
        tags=("Map", "Planning", "Internal"),
        note="Internal planning map. Not intended for public distribution.",
        internal=True,
    ),
    Project(
        slug="mirrors",
        name="Runchero Mirrors",
        tagline="Save the websites our community relies on.",
        description=(
            "Paste a website address and the depot copies it slowly and politely, so "
            "the pages stay readable on the local network when the internet does not. "
            "Good for manuals, guides, and reference sites."
        ),
        port=8090,
        icon="archive.png",
        screenshot="mirrors.png",
        tags=("Archive", "Offline", "Websites"),
    ),
    Project(
        slug="links",
        name="Runchero Links",
        tagline="Turn everyday Amazon links into community support.",
        description=(
            "Convert Amazon product links and searches into clean tagged affiliate "
            "links, with bulk conversion, a search bar, and a plain-language earnings "
            "estimator. Stateless: nothing is stored."
        ),
        port=8091,
        icon="tag.png",
        screenshot="links.png",
        tags=("Affiliate", "Tools", "Money"),
    ),
    Project(
        slug="community",
        name="Runchero Community Directory",
        tagline="The people of Runchero, all in one place.",
        description=(
            "A neighbours-only directory for the local network. People can add "
            "themselves with phone, email, social links, and a website. Businesses, "
            "groups, and services are not listed. Entries are locked after submission, "
            "and an admin can edit, hide, or remove them."
        ),
        port=8093,
        icon="chat.png",
        screenshot="community.png",
        tags=("People", "Neighbours", "Contact"),
    ),
]


def is_excluded(text: str) -> bool:
    lowered = (text or "").lower()
    return any(token in lowered for token in config.EXCLUDED_TOKENS)


def visible_projects() -> list[Project]:
    safe = []
    for project in PROJECTS:
        haystack = " ".join(
            [project.slug, project.name, project.tagline, project.description]
            + list(project.tags)
        )
        if is_excluded(haystack):
            continue
        safe.append(project)
    return safe


def find(slug: str) -> Project | None:
    for project in visible_projects():
        if project.slug == slug:
            return project
    return None


def project_url(project: Project, request_host: str) -> str:
    host = config.LINK_HOST or request_host or "127.0.0.1"
    parsed = urlsplit("//" + host)
    hostname = parsed.hostname or host
    return f"http://{hostname}:{project.port}{project.path}"
