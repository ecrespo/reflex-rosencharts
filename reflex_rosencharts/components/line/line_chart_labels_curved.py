"""line_chart_labels_curved — port of line-charts/4_LineChartLabelsCurved.tsx.

Render technique: SVG path computed with D3 (``curveMonotoneX``), with an HTML
overlay that places a small rounded value-badge over each point. No tooltip, so
this is a plain ``rx.Component``.

Data schema (``LinePoint``)::

    {"date": "YYYY-MM-DD", "value": float}

Example::

    import reflex_rosencharts as rxc
    rxc.line_chart_labels_curved(data=State.sales)
"""

from typing import TypedDict

import reflex as rx


class LinePoint(TypedDict):
    """A single point of a time series."""

    date: str  # ISO date 'YYYY-MM-DD'
    value: float


_DEFAULT_DATA: list[LinePoint] = [
    {"date": "2023-04-30", "value": 3},
    {"date": "2023-05-01", "value": 6},
    {"date": "2023-05-02", "value": 8},
    {"date": "2023-05-03", "value": 6},
    {"date": "2023-05-04", "value": 10},
    {"date": "2023-05-05", "value": 12},
    {"date": "2023-05-06", "value": 11},
    {"date": "2023-05-07", "value": 8},
    {"date": "2023-05-08", "value": 4},
    {"date": "2023-05-09", "value": 9},
    {"date": "2023-05-10", "value": 9},
]

_PATH = rx.asset("line_chart_labels_curved.tsx", shared=True)


class LineChartLabelsCurved(rx.Component):
    """Reflex wrapper around the parametrized LineChartLabelsCurved TSX."""

    library = f"$/public{_PATH}"
    tag = "LineChartLabelsCurved"
    is_default = False

    lib_dependencies: list[str] = ["d3"]

    data: rx.Var[list[LinePoint]] = rx.Var.create(_DEFAULT_DATA)
    color: rx.Var[str] = rx.Var.create("text-purple-300")


def line_chart_labels_curved(**props) -> rx.Component:
    """Smooth line chart with a value badge rendered over every point.

    Args:
        data: list of ``{"date": "YYYY-MM-DD", "value": float}``. Defaults to the
            original rosencharts example.
        color: Tailwind ``text-*`` class for the line (drawn via currentColor).
            Defaults to ``"text-purple-300"``.

    Returns:
        A Reflex component rendering the labelled curved line chart.
    """
    return LineChartLabelsCurved.create(**props)
