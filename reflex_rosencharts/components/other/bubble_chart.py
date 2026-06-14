"""bubble_chart — port of rosencharts other-charts/4_BubbleChart_DIV.tsx to Reflex.

Render technique: a bubble (circle-packed scatter) where each datum becomes an
absolutely-positioned ``<div>`` circle. The layout is computed with ``d3.pack()``
over a flat hierarchy summed by ``value``; circle area encodes ``value`` and the
fill color encodes ``sector`` (ordinal scale). The original file name carries a
``_DIV`` suffix to note the DIV-based render technique; we drop it for the public
function name.

Data schema (``BubblePoint``)::

    {"name": str, "sector": str, "value": float}

Example::

    import reflex_rosencharts as rxc
    rxc.bubble_chart(data=State.holdings)
"""

from typing import TypedDict

import reflex as rx


class BubblePoint(TypedDict):
    """A single bubble: a labelled value grouped by sector."""

    name: str
    sector: str
    value: float


# Default dataset == the original rosencharts example, so ``bubble_chart()`` with no
# args reproduces the reference chart (Tech Design DD-002).
_DEFAULT_DATA: list[BubblePoint] = [
    {"name": "MacOS", "sector": "Tech", "value": 4812},
    {"name": "Linux", "sector": "Tech", "value": 3212},
    {"name": "Windows", "sector": "Tech", "value": 512},
    {"name": "Diesel", "sector": "Energy", "value": 1252},
    {"name": "Petrol", "sector": "Energy", "value": 625},
    {"name": "Diesel", "sector": "Utilities", "value": 1252},
    {"name": "Petrol", "sector": "Utilities", "value": 825},
    {"name": "Bonds", "sector": "Cyclicals", "value": 1517},
    {"name": "Loans", "sector": "Cyclicals", "value": 1213},
    {"name": "Loans", "sector": "Cyclicals", "value": 213},
    {"name": "Petrol", "sector": "Energy", "value": 1825},
    {"name": "Bonds", "sector": "Financials", "value": 2517},
    {"name": "Loans", "sector": "Financials", "value": 1213},
    {"name": "Loans", "sector": "Financials", "value": 613},
    {"name": "Petrol", "sector": "Energy", "value": 825},
    {"name": "Bonds", "sector": "Financials", "value": 1817},
    {"name": "Loans", "sector": "Financials", "value": 1213},
    {"name": "Loans", "sector": "Utilities", "value": 213},
]

_DEFAULT_COLORS: list[str] = [
    "text-pink-400",
    "text-violet-500",
    "text-lime-500",
    "text-sky-400",
    "text-orange-400",
]

_PATH = rx.asset("bubble_chart.tsx", shared=True)


class BubbleChart(rx.Component):
    """Reflex wrapper around the parametrized BubbleChart TSX."""

    library = f"$/public{_PATH}"
    tag = "BubbleChart"
    is_default = False

    lib_dependencies: list[str] = ["d3"]

    # Props
    data: rx.Var[list[BubblePoint]] = rx.Var.create(_DEFAULT_DATA)
    colors: rx.Var[list[str]] = rx.Var.create(_DEFAULT_COLORS)


def bubble_chart(**props) -> rx.Component:
    """Circle-packed bubble chart (DIV-based) grouped by sector.

    Args:
        data: list of ``{"name": str, "sector": str, "value": float}``. Circle area
            encodes ``value``; defaults to the original rosencharts example.
        colors: ordinal Tailwind ``text-*`` palette applied per ``sector``. Defaults
            to the original 5-color palette.

    Returns:
        A Reflex component rendering the bubble chart.
    """
    return BubbleChart.create(**props)
