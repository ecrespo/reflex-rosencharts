"""bar_chart_line — port of rosencharts bar-charts/14_BarChartLine.tsx.

Render technique: DIV vertical bars for ``metric1`` (left axis) overlaid with a D3
``curveMonotoneX`` SVG line for ``metric2`` (right axis). Uses the shared
ClientTooltip helper (client-side only, NoSSRComponent).

Data schema (``BarLineItem``)::

    {"key": str, "metric1": float, "metric2": float}

Example::

    import reflex_rosencharts as rxc
    rxc.bar_chart_line(data=State.monthly)
"""

from typing import TypedDict

import reflex as rx

from ..helpers.client_tooltip import client_tooltip_asset


class BarLineItem(TypedDict):
    """A bar (metric1) plus an overlaid line value (metric2) per category."""

    key: str
    metric1: float
    metric2: float


_DEFAULT_DATA: list[BarLineItem] = [
    {"key": "Jan", "metric1": 18.1, "metric2": 700},
    {"key": "Feb", "metric1": 14.3, "metric2": 1000},
    {"key": "Mar", "metric1": 27.1, "metric2": 900},
    {"key": "Apr", "metric1": 40, "metric2": 1000},
    {"key": "May", "metric1": 12.7, "metric2": 500},
    {"key": "Jun", "metric1": 22.8, "metric2": 600},
    {"key": "Jul", "metric1": 17.8, "metric2": 900},
    {"key": "Aug", "metric1": 5.8, "metric2": 800},
    {"key": "Sep", "metric1": 42, "metric2": 700},
    {"key": "Oct", "metric1": 12.7, "metric2": 900},
    {"key": "Nov", "metric1": 24.7, "metric2": 1000},
    {"key": "Dec", "metric1": 19.7, "metric2": 1220},
]

client_tooltip_asset()
_PATH = rx.asset("bar_chart_line.tsx", shared=True)


class BarChartLine(rx.NoSSRComponent):
    """Reflex wrapper around the parametrized BarChartLine TSX."""

    library = f"$/public{_PATH}"
    tag = "BarChartLine"
    is_default = False

    lib_dependencies: list[str] = ["d3"]

    data: rx.Var[list[BarLineItem]] = rx.Var.create(_DEFAULT_DATA)


def bar_chart_line(**props) -> rx.Component:
    """Vertical bars (metric1) overlaid with a smooth line (metric2), dual y-axes.

    Args:
        data: list of ``{"key": str, "metric1": float, "metric2": float}``. Defaults to
            the original rosencharts example. Bars padded to a minimum of 10.

    Returns:
        A Reflex component rendering the bar+line combo chart.
    """
    return BarChartLine.create(**props)
