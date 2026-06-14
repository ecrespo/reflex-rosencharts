"""line_chart_step — port of rosencharts line-charts/6_LineChartStep.tsx.

Render technique: SVG path computed with D3 (``curveStep``) drawn with an
emerald→lime ``linearGradient`` stroke, styled with Tailwind. Uses the shared
ClientTooltip helper (createPortal), so the component is client-side only
(NoSSRComponent).

Data schema (``LinePoint``)::

    {"date": "YYYY-MM-DD", "value": float}

Example::

    import reflex_rosencharts as rxc
    rxc.line_chart_step(data=State.sales)
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
    {"date": "2023-05-07", "value": 8},
    {"date": "2023-05-08", "value": 7},
    {"date": "2023-05-09", "value": 9},
]

client_tooltip_asset()
_PATH = rx.asset("line_chart_step.tsx", shared=True)


class LineChartStep(rx.NoSSRComponent):
    """Reflex wrapper around the parametrized LineChartStep TSX."""

    library = f"$/public{_PATH}"
    tag = "LineChartStep"
    is_default = False

    lib_dependencies: list[str] = ["d3"]

    data: rx.Var[list[LinePoint]] = rx.Var.create(_DEFAULT_DATA)


def line_chart_step(**props) -> rx.Component:
    """Step-interpolated time-series line chart with a per-point tooltip.

    Args:
        data: list of ``{"date": "YYYY-MM-DD", "value": float}``. Defaults to the
            original rosencharts example.

    Returns:
        A Reflex component rendering the step line chart.
    """
    return LineChartStep.create(**props)
