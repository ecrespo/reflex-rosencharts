"""bar_chart_thin_horizontal — port of bar-charts/6_BarChartThinHorizontal_DIV.tsx.

Render technique: DIV-based thin bars with D3 scales; bar color is chosen by width
bucket. Uses the shared ClientTooltip helper (client-side only, NoSSRComponent). The
``_DIV`` suffix is dropped (render technique only).

Data schema (``BarItem``)::

    {"key": str, "value": float}

The chart sorts descending by value internally.

Example::

    import reflex_rosencharts as rxc
    rxc.bar_chart_thin_horizontal(data=State.countries)
"""

from typing import TypedDict

import reflex as rx

from ..helpers.client_tooltip import client_tooltip_asset


class BarItem(TypedDict):
    """A single bar: a category key and its value."""

    key: str
    value: float


_DEFAULT_DATA: list[BarItem] = [
    {"key": "France", "value": 38.1},
    {"key": "Spain", "value": 25.3},
    {"key": "Italy", "value": 23.1},
    {"key": "Portugal", "value": 19.5},
    {"key": "Germany", "value": 14.7},
    {"key": "Netherlands", "value": 6.1},
    {"key": "Belgium", "value": 10.8},
    {"key": "Austria", "value": 7.8},
    {"key": "Greece", "value": 6.8},
    {"key": "Luxembourg", "value": 5.5},
    {"key": "Cyprus", "value": 4.8},
    {"key": "Malta", "value": 3.5},
    {"key": "Slovenia", "value": 3.8},
    {"key": "Estonia", "value": 8.8},
    {"key": "Latvia", "value": 15.8},
    {"key": "Lithuania", "value": 12.8},
    {"key": "Croatia", "value": 5.8},
]

client_tooltip_asset()
_PATH = rx.asset("bar_chart_thin_horizontal.tsx", shared=True)


class BarChartThinHorizontal(rx.NoSSRComponent):
    """Reflex wrapper around the parametrized BarChartThinHorizontal TSX."""

    library = f"$/public{_PATH}"
    tag = "BarChartThinHorizontal"
    is_default = False

    lib_dependencies: list[str] = ["d3"]

    data: rx.Var[list[BarItem]] = rx.Var.create(_DEFAULT_DATA)


def bar_chart_thin_horizontal(**props) -> rx.Component:
    """Thin horizontal bar chart (color by width bucket) with a per-bar tooltip.

    Args:
        data: list of ``{"key": str, "value": float}``. Defaults to the original
            rosencharts example. Sorted descending by value internally.

    Returns:
        A Reflex component rendering the thin horizontal bar chart.
    """
    return BarChartThinHorizontal.create(**props)
