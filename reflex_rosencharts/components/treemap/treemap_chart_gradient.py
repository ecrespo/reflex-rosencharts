"""treemap_chart_gradient — port of rosencharts treemap-charts/3_TreemapChartGradient_DIV.tsx.

Render technique: a D3 treemap layout (``d3.treemap``) rendered as absolutely
positioned ``<div>`` cells styled with Tailwind gradient classes per topic (the
original ``_DIV`` variant; the suffix denotes the render technique and is dropped from
the public name). Uses the shared ClientTooltip helper (createPortal), so the
component renders client-side only (NoSSRComponent).

Data schema (``TreemapGradientNode``)::

    {"topic": "Tech", "subtopics": [{"name": "Apple", "value": 100}]}

Here ``subtopics`` is a list of ``{name, value}`` dicts (one per leaf).

Example::

    import reflex_rosencharts as rxc
    rxc.treemap_chart_gradient(data=State.sectors)
"""

from typing import TypedDict

import reflex as rx

from ..helpers.client_tooltip import client_tooltip_asset


class TreemapGradientSubtopic(TypedDict):
    """A single leaf name/value."""

    name: str
    value: float


class TreemapGradientNode(TypedDict):
    """A topic with a list of ``{name, value}`` subtopics."""

    topic: str
    subtopics: list[TreemapGradientSubtopic]


# Default dataset == the original rosencharts example.
_DEFAULT_DATA: list[TreemapGradientNode] = [
    {
        "topic": "Tech",
        "subtopics": [
            {"name": "Apple", "value": 100},
            {"name": "Mercedes", "value": 120},
            {"name": "Palantir", "value": 110},
        ],
    },
    {
        "topic": "Financials",
        "subtopics": [
            {"name": "Tesla", "value": 60},
            {"name": "Meta", "value": 70},
            {"name": "Google", "value": 20},
        ],
    },
    {
        "topic": "Energy",
        "subtopics": [
            {"name": "Apple", "value": 70},
            {"name": "Mercedes", "value": 50},
            {"name": "Palantir", "value": 20},
            {"name": "Google", "value": 100},
        ],
    },
]

_DEFAULT_COLORS: list[str] = [
    "bg-gradient-to-b from-purple-400 to-purple-500 text-white dark:from-purple-500 dark:to-purple-700 dark:text-purple-100",
    "bg-gradient-to-b from-pink-300 to-pink-400 text-white dark:from-pink-500 dark:to-pink-600 dark:text-pink-100",
    "bg-gradient-to-b from-orange-300 to-orange-400 text-white dark:from-amber-500 dark:to-amber-600 dark:text-amber-100",
]

# Ship the shared helper next to this chart so the TSX relative import resolves.
client_tooltip_asset()
_PATH = rx.asset("treemap_chart_gradient.tsx", shared=True)


class TreemapChartGradient(rx.NoSSRComponent):
    """Reflex wrapper around the parametrized TreemapChartGradient TSX."""

    library = f"$/public{_PATH}"
    tag = "TreemapChartGradient"
    is_default = False

    lib_dependencies: list[str] = ["d3"]

    # Props
    data: rx.Var[list[TreemapGradientNode]] = rx.Var.create(_DEFAULT_DATA)
    colors: rx.Var[list[str]] = rx.Var.create(_DEFAULT_COLORS)


def treemap_chart_gradient(**props) -> rx.Component:
    """Treemap with Tailwind gradient cells per topic and a per-cell tooltip.

    Args:
        data: list of ``{"topic": str, "subtopics": [{name, value}]}``.
            Defaults to the original rosencharts example.
        colors: Tailwind gradient classes, one per topic. Defaults to the original
            purple/pink/orange gradients.

    Returns:
        A Reflex component rendering the gradient treemap chart.
    """
    return TreemapChartGradient.create(**props)
