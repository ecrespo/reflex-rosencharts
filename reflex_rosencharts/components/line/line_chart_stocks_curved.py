"""line_chart_stocks_curved — port of line-charts/5_LineChartStocksCurved.tsx.

Render technique: SVG path computed with D3 (``curveMonotoneX``), with an HTML
overlay placing a small company-logo glyph over each point. The logo glyphs are
a fixed decorative set cycled by point index (not data-driven). No tooltip, so
this is a plain ``rx.Component``.

Data schema (``LinePoint``)::

    {"date": "YYYY-MM-DD", "value": float}

Example::

    import reflex_rosencharts as rxc
    rxc.line_chart_stocks_curved(data=State.prices)
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

_PATH = rx.asset("line_chart_stocks_curved.tsx", shared=True)


class LineChartStocksCurved(rx.Component):
    """Reflex wrapper around the parametrized LineChartStocksCurved TSX."""

    library = f"$/public{_PATH}"
    tag = "LineChartStocksCurved"
    is_default = False

    lib_dependencies: list[str] = ["d3"]

    data: rx.Var[list[LinePoint]] = rx.Var.create(_DEFAULT_DATA)
    color: rx.Var[str] = rx.Var.create("stroke-gray-400")


def line_chart_stocks_curved(**props) -> rx.Component:
    """Smooth stock-style line chart with a company-logo glyph over each point.

    Args:
        data: list of ``{"date": "YYYY-MM-DD", "value": float}``. Defaults to the
            original rosencharts example.
        color: Tailwind ``stroke-*`` class for the line. Defaults to
            ``"stroke-gray-400"``.

    Returns:
        A Reflex component rendering the stocks line chart.
    """
    return LineChartStocksCurved.create(**props)
