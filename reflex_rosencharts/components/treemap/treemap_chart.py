"""treemap_chart — port of rosencharts treemap-charts/1_TreemapChart_DIV.tsx.

Render technique: a D3 treemap layout (``d3.treemap``) rendered as absolutely
positioned ``<div>`` cells styled with Tailwind (the original ``_DIV`` variant; the
suffix denotes the render technique and is dropped from the public name). Uses the
shared ClientTooltip helper (createPortal), so the component renders client-side only
(NoSSRComponent).

Data schema (``TreemapNode``)::

    {"topic": "Tech", "subtopics": [{"Windows": 100, "MacOS": 120, "Linux": 110}]}

``subtopics`` is a one-element list whose dict maps each leaf name to its numeric
value.

Example::

    import reflex_rosencharts as rxc
    rxc.treemap_chart(data=State.portfolio)
"""

from typing import TypedDict

import reflex as rx

from ..helpers.client_tooltip import client_tooltip_asset


class TreemapNode(TypedDict):
    """A topic with one dict of ``{leaf_name: value}`` subtopics."""

    topic: str
    subtopics: list[dict]


# Default dataset == the original rosencharts example.
_DEFAULT_DATA: list[TreemapNode] = [
    {"topic": "Tech", "subtopics": [{"Windows": 100, "MacOS": 120, "Linux": 110}]},
    {"topic": "Financials", "subtopics": [{"Loans": 60, "Bonds": 80, "PPRs": 20}]},
    {"topic": "Energy", "subtopics": [{"Petrol": 70, "Diesel": 50, "Hydrogen": 20}]},
]

_DEFAULT_COLORS: list[str] = [
    "bg-violet-500 dark:bg-violet-500",
    "bg-pink-400 dark:bg-pink-400",
    "bg-orange-400 dark:bg-orange-400",
]

# Ship the shared helper next to this chart so the TSX relative import resolves.
client_tooltip_asset()
_PATH = rx.asset("treemap_chart.tsx", shared=True)


class TreemapChart(rx.NoSSRComponent):
    """Reflex wrapper around the parametrized TreemapChart TSX."""

    library = f"$/public{_PATH}"
    tag = "TreemapChart"
    is_default = False

    lib_dependencies: list[str] = ["d3"]

    # Props
    data: rx.Var[list[TreemapNode]] = rx.Var.create(_DEFAULT_DATA)
    colors: rx.Var[list[str]] = rx.Var.create(_DEFAULT_COLORS)


def treemap_chart(**props) -> rx.Component:
    """Treemap of nested topics/subtopics with a per-cell tooltip.

    Args:
        data: list of ``{"topic": str, "subtopics": [{name: value, ...}]}``.
            Defaults to the original rosencharts example.
        colors: Tailwind ``bg-*`` classes, one per topic. Defaults to the original
            violet/pink/orange palette.

    Returns:
        A Reflex component rendering the treemap chart.
    """
    return TreemapChart.create(**props)
