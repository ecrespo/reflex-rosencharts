"""line_chart_curved — port of rosencharts line-charts/2_LineChartCurved.tsx.

Render technique: SVG path computed with D3 (scaleTime/scaleLinear/d3.line with
``curveMonotoneX`` for a smooth curve), styled with Tailwind. Uses the shared
ClientTooltip helper (createPortal), so the component is client-side only
(NoSSRComponent).

Data schema (``LinePoint``)::

    {"date": "YYYY-MM-DD", "value": float}

Example::

    import reflex_rosencharts as rxc
    rxc.line_chart_curved(data=State.sales, color="stroke-violet-400")
"""

from typing import TypedDict

import reflex as rx

from ..helpers.client_tooltip import client_tooltip_asset


class LinePoint(TypedDict):
    """A single point of a time series."""

    date: str  # ISO date 'YYYY-MM-DD'
    value: float


_DEFAULT_DATA: list[LinePoint] = [
    {"date": "2023-04-30", "value": 4},
    {"date": "2023-05-01", "value": 2},
    {"date": "2023-05-02", "value": 8},
    {"date": "2023-05-03", "value": 7},
    {"date": "2023-05-04", "value": 10},
    {"date": "2023-05-05", "value": 12},
    {"date": "2023-05-06", "value": 11},
    {"date": "2023-05-07", "value": 8},
    {"date": "2023-05-08", "value": 7},
    {"date": "2023-05-09", "value": 9},
]

client_tooltip_asset()
_PATH = rx.asset("line_chart_curved.tsx", shared=True)


class LineChartCurved(rx.NoSSRComponent):
    """Reflex wrapper around the parametrized LineChartCurved TSX."""

    library = f"$/public{_PATH}"
    tag = "LineChartCurved"
    is_default = False

    lib_dependencies: list[str] = ["d3"]

    data: rx.Var[list[LinePoint]] = rx.Var.create(_DEFAULT_DATA)
    color: rx.Var[str] = rx.Var.create("stroke-violet-400")


def line_chart_curved(**props) -> rx.Component:
    """Smooth (monotone) time-series line chart with a per-point tooltip.

    Args:
        data: list of ``{"date": "YYYY-MM-DD", "value": float}``. Defaults to the
            original rosencharts example.
        color: Tailwind ``stroke-*`` class for the line. Defaults to
            ``"stroke-violet-400"``.

    Returns:
        A Reflex component rendering the curved line chart.
    """
    return LineChartCurved.create(**props)
