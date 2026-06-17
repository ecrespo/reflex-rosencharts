"""scatter_chart_stocks — port of rosencharts scatter-charts/6_ScatterChartStocks.tsx.

Render technique: D3 ``scaleLinear`` on both axes; instead of dots, each point is
rendered as an inline company-logo SVG positioned with absolute CSS, cycling through a
built-in set of logos. Uses the shared ClientTooltip helper (createPortal) → rendered
client-side only (NoSSRComponent).

Data schema (``ScatterPoint``)::

    {"revenue": float (x), "value": float (y), "company": str}

Example::

    import reflex_rosencharts as rxc
    rxc.scatter_chart_stocks(data=State.points)
"""

from typing import TypedDict

import reflex as rx

from ..helpers.client_tooltip import client_tooltip_asset


class ScatterPoint(TypedDict):
    """A single scatter point: x=revenue, y=value, label=company."""

    revenue: float
    value: float
    company: str


# Default dataset == the original rosencharts example.
_DEFAULT_DATA: list[ScatterPoint] = [
    {"revenue": 10, "value": 500, "company": "Company A"},
    {"revenue": 20, "value": 800, "company": "Company B"},
    {"revenue": 30, "value": 400, "company": "Company C"},
    {"revenue": 40, "value": 650, "company": "Company D"},
    {"revenue": 50, "value": 500, "company": "Company E"},
    {"revenue": 60, "value": 850, "company": "Spanish or vanish"},
    {"revenue": 70, "value": 450, "company": "Company G"},
    {"revenue": 80, "value": 750, "company": "Company H"},
    {"revenue": 90, "value": 350, "company": "Company I"},
    {"revenue": 100, "value": 700, "company": "Company J"},
]

client_tooltip_asset()
_PATH = rx.asset("scatter_chart_stocks.tsx", shared=True)


class ScatterChartStocks(rx.NoSSRComponent):
    """Reflex wrapper around the parametrized ScatterChartStocks TSX."""

    library = f"$/public{_PATH}"
    tag = "ScatterChartStocks"
    is_default = False

    lib_dependencies: list[str] = ["d3"]

    data: rx.Var[list[ScatterPoint]] = rx.Var.create(_DEFAULT_DATA)


def scatter_chart_stocks(**props) -> rx.Component:
    """Scatter plot rendering each point as a cycling company-logo badge.

    Args:
        data: list of ``{"revenue": x, "value": y, "company": label}``. Defaults to
            the original rosencharts example.

    Returns:
        A Reflex component rendering the stocks scatter chart.
    """
    return ScatterChartStocks.create(**props)
