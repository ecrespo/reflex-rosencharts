"""bar_chart_horizontal — port of rosencharts bar-charts/1_BarChartHorizontal_DIV.tsx.

Render technique: DIV-based (absolutely positioned ``<div>`` bars, no SVG paths),
with D3 ``scaleBand``/``scaleLinear`` for layout. Uses the shared ClientTooltip helper
(createPortal), so the component is client-side only (NoSSRComponent). The original
``_DIV`` suffix is dropped; it only denotes the render technique.

Data schema (``BarItem``)::

    {"key": str, "value": float}

The chart sorts descending by value internally.

Example::

    import reflex_rosencharts as rxc
    rxc.bar_chart_horizontal(data=State.sectors)
"""

from typing import TypedDict

import reflex as rx

from ..helpers.client_tooltip import client_tooltip_asset


class BarItem(TypedDict):
    """A single bar: a category key and its value."""

    key: str
    value: float


_DEFAULT_DATA: list[BarItem] = [
    {"key": "Technology", "value": 38.1},
    {"key": "Financials", "value": 25.3},
    {"key": "Energy", "value": 23.1},
    {"key": "Cyclical", "value": 19.5},
    {"key": "Defensive", "value": 14.7},
    {"key": "Utilities", "value": 5.8},
]

client_tooltip_asset()
_PATH = rx.asset("bar_chart_horizontal.tsx", shared=True)


class BarChartHorizontal(rx.NoSSRComponent):
    """Reflex wrapper around the parametrized BarChartHorizontal TSX."""

    library = f"$/public{_PATH}"
    tag = "BarChartHorizontal"
    is_default = False

    lib_dependencies: list[str] = ["d3"]

    data: rx.Var[list[BarItem]] = rx.Var.create(_DEFAULT_DATA)


def bar_chart_horizontal(**props) -> rx.Component:
    """Horizontal bar chart with a per-bar tooltip.

    Args:
        data: list of ``{"key": str, "value": float}``. Defaults to the original
            rosencharts example. Sorted descending by value internally.

    Returns:
        A Reflex component rendering the horizontal bar chart.
    """
    return BarChartHorizontal.create(**props)
