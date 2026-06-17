"""treemap_chart_images — port of rosencharts treemap-charts/2_TreemapChartImages_DIV.tsx.

Render technique: a D3 treemap layout (``d3.treemap``) rendered as absolutely
positioned ``<div>`` cells styled with Tailwind, each leaf showing a logo image (the
original ``_DIV`` variant; the suffix denotes the render technique and is dropped from
the public name). Uses the shared ClientTooltip helper (createPortal), so the
component renders client-side only (NoSSRComponent).

Data schema (``TreemapImageNode``)::

    {"topic": "Tech", "subtopics": [{"name": "Apple", "value": 100, "logo": "https://.../a.svg"}]}

Here ``subtopics`` is a list of ``{name, value, logo}`` dicts (one per leaf).

Example::

    import reflex_rosencharts as rxc
    rxc.treemap_chart_images(data=State.holdings)
"""

from typing import TypedDict

import reflex as rx

from ..helpers.client_tooltip import client_tooltip_asset


class TreemapImageSubtopic(TypedDict):
    """A single leaf with its logo URL."""

    name: str
    value: float
    logo: str


class TreemapImageNode(TypedDict):
    """A topic with a list of ``{name, value, logo}`` subtopics."""

    topic: str
    subtopics: list[TreemapImageSubtopic]


_AVATARS = "https://etoro-cdn.etorostatic.com/market-avatars"

# Default dataset == the original rosencharts example.
_DEFAULT_DATA: list[TreemapImageNode] = [
    {
        "topic": "Tech",
        "subtopics": [
            {"name": "Apple", "value": 100, "logo": f"{_AVATARS}/1001/1001_494D5A_F7F7F7.svg"},
            {"name": "Mercedes", "value": 120, "logo": f"{_AVATARS}/1206/1206_2F3350_F7F7F7.svg"},
            {"name": "Palantir", "value": 110, "logo": f"{_AVATARS}/7991/7991_2C2C2C_F7F7F7.svg"},
        ],
    },
    {
        "topic": "Financials",
        "subtopics": [
            {"name": "Nvidia", "value": 70, "logo": f"{_AVATARS}/1137/1137_76B900_F7F7F7.svg"},
            {"name": "AMD", "value": 60, "logo": f"{_AVATARS}/1832/1832_2C2C2C_F7F7F7.svg"},
            {"name": "Google", "value": 20, "logo": f"{_AVATARS}/1002/1002_3183FF_F7F7F7.svg"},
        ],
    },
    {
        "topic": "Energy",
        "subtopics": [
            {"name": "Apple", "value": 70, "logo": f"{_AVATARS}/1001/1001_494D5A_F7F7F7.svg"},
            {"name": "Mercedes", "value": 50, "logo": f"{_AVATARS}/1206/1206_2F3350_F7F7F7.svg"},
            {"name": "Palantir", "value": 20, "logo": f"{_AVATARS}/7991/7991_2C2C2C_F7F7F7.svg"},
            {"name": "Google", "value": 100, "logo": f"{_AVATARS}/1002/1002_3183FF_F7F7F7.svg"},
        ],
    },
]

_DEFAULT_COLORS: list[str] = [
    "bg-violet-500 dark:bg-violet-500",
    "bg-pink-400 dark:bg-pink-400",
    "bg-orange-400 dark:bg-orange-400",
]

# Ship the shared helper next to this chart so the TSX relative import resolves.
client_tooltip_asset()
_PATH = rx.asset("treemap_chart_images.tsx", shared=True)


class TreemapChartImages(rx.NoSSRComponent):
    """Reflex wrapper around the parametrized TreemapChartImages TSX."""

    library = f"$/public{_PATH}"
    tag = "TreemapChartImages"
    is_default = False

    lib_dependencies: list[str] = ["d3"]

    # Props
    data: rx.Var[list[TreemapImageNode]] = rx.Var.create(_DEFAULT_DATA)
    colors: rx.Var[list[str]] = rx.Var.create(_DEFAULT_COLORS)


def treemap_chart_images(**props) -> rx.Component:
    """Treemap whose leaf cells display a logo image, with a per-cell tooltip.

    Args:
        data: list of ``{"topic": str, "subtopics": [{name, value, logo}]}``.
            Defaults to the original rosencharts example.
        colors: Tailwind ``bg-*`` classes, one per topic. Defaults to the original
            violet/pink/orange palette.

    Returns:
        A Reflex component rendering the image treemap chart.
    """
    return TreemapChartImages.create(**props)
