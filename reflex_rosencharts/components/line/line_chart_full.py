"""line_chart_full — port of rosencharts line-charts/8_LineChartFull.tsx.

Render technique: full-bleed SVG path computed with D3 (``curveNatural``) drawn
with a purple→pink ``linearGradient`` stroke, with grid lines and lightweight
in-chart X/Y axis labels. No tooltip, so this is a plain ``rx.Component``.

Data schema (``LinePoint``)::

    {"date": "YYYY-MM-DD", "value": float}

Example::

    import reflex_rosencharts as rxc
    rxc.line_chart_full(data=State.series)
"""

from typing import TypedDict

import reflex as rx


class LinePoint(TypedDict):
    """A single point of a time series."""

    date: str  # ISO date 'YYYY-MM-DD'
    value: float


_DEFAULT_DATA: list[LinePoint] = [
    {"date": "2023-04-30", "value": 5},
    {"date": "2023-05-01", "value": 7},
    {"date": "2023-05-02", "value": 7},
    {"date": "2023-05-03", "value": 7.5},
    {"date": "2023-05-04", "value": 9},
    {"date": "2023-05-05", "value": 10.5},
    {"date": "2023-05-06", "value": 11},
    {"date": "2023-05-07", "value": 10.5},
    {"date": "2023-05-08", "value": 8},
    {"date": "2023-05-09", "value": 9},
    {"date": "2023-05-10", "value": 9.5},
    {"date": "2023-05-11", "value": 10},
    {"date": "2023-05-12", "value": 9},
    {"date": "2023-05-13", "value": 8.5},
    {"date": "2023-05-14", "value": 6},
    {"date": "2023-05-15", "value": 7},
    {"date": "2023-05-16", "value": 9},
    {"date": "2023-05-17", "value": 10},
    {"date": "2023-05-18", "value": 10.5},
    {"date": "2023-05-19", "value": 11},
    {"date": "2023-05-20", "value": 11},
    {"date": "2023-05-21", "value": 11.5},
    {"date": "2023-05-22", "value": 12},
    {"date": "2023-05-23", "value": 12},
]

_PATH = rx.asset("line_chart_full.tsx", shared=True)


class LineChartFull(rx.Component):
    """Reflex wrapper around the parametrized LineChartFull TSX."""

    library = f"$/public{_PATH}"
    tag = "LineChartFull"
    is_default = False

    lib_dependencies: list[str] = ["d3"]

    data: rx.Var[list[LinePoint]] = rx.Var.create(_DEFAULT_DATA)


def line_chart_full(**props) -> rx.Component:
    """Full-bleed gradient line chart with in-chart axes (natural curve).

    Args:
        data: list of ``{"date": "YYYY-MM-DD", "value": float}``. Defaults to the
            original rosencharts example.

    Returns:
        A Reflex component rendering the full line chart.
    """
    return LineChartFull.create(**props)
