"""line_chart_pulse — port of rosencharts line-charts/7_LineChartPulse.tsx.

Render technique: SVG path computed with D3 (``curveNatural``) drawn with a
purple→pink ``linearGradient`` stroke, plus an ``animate-ping`` pulsating dot at
the last point. Uses the shared ClientTooltip helper (createPortal), so the
component is client-side only (NoSSRComponent).

Data schema (``LinePoint``)::

    {"date": "YYYY-MM-DD", "value": float}

Example::

    import reflex_rosencharts as rxc
    rxc.line_chart_pulse(data=State.sales)
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
    {"date": "2023-05-01", "value": 6},
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
_PATH = rx.asset("line_chart_pulse.tsx", shared=True)


class LineChartPulse(rx.NoSSRComponent):
    """Reflex wrapper around the parametrized LineChartPulse TSX."""

    library = f"$/public{_PATH}"
    tag = "LineChartPulse"
    is_default = False

    lib_dependencies: list[str] = ["d3"]

    data: rx.Var[list[LinePoint]] = rx.Var.create(_DEFAULT_DATA)


def line_chart_pulse(**props) -> rx.Component:
    """Smooth (natural) line chart with a pulsating last-point dot and tooltip.

    Args:
        data: list of ``{"date": "YYYY-MM-DD", "value": float}``. Defaults to the
            original rosencharts example.

    Returns:
        A Reflex component rendering the pulse line chart.
    """
    return LineChartPulse.create(**props)
