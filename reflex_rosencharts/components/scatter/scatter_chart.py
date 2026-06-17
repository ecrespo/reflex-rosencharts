"""scatter_chart — port of rosencharts scatter-charts/1_ScatterChart.tsx to Reflex.

Render technique: SVG points (D3 ``scaleLinear`` on both axes) plotted in a
0-100 viewBox, styled with Tailwind. Uses the shared ClientTooltip helper
(createPortal), so the component is rendered client-side only (NoSSRComponent).

Data schema (``ScatterPoint``)::

    {"revenue": float (x), "value": float (y), "company": str}

Example::

    import reflex_rosencharts as rxc
    rxc.scatter_chart(data=State.points, color="text-violet-400")
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
    {"revenue": 10, "value": 102.8, "company": "Company A"},
    {"revenue": 20, "value": 101.9, "company": "Company B"},
    {"revenue": 30, "value": 101.5, "company": "Company C"},
    {"revenue": 40, "value": 100.2, "company": "Company D"},
    {"revenue": 50, "value": 100.8, "company": "Company E"},
    {"revenue": 60, "value": 99.7, "company": "Company F"},
    {"revenue": 70, "value": 99.9, "company": "Company G"},
    {"revenue": 80, "value": 98.5, "company": "Company H"},
    {"revenue": 90, "value": 98.9, "company": "Company I"},
    {"revenue": 100, "value": 97.8, "company": "Company J"},
    {"revenue": 110, "value": 98.2, "company": "Company K"},
    {"revenue": 120, "value": 96.8, "company": "Company L"},
    {"revenue": 130, "value": 96.9, "company": "Company M"},
    {"revenue": 140, "value": 95.5, "company": "Company N"},
    {"revenue": 150, "value": 95.9, "company": "Company O"},
    {"revenue": 160, "value": 94.5, "company": "Company P"},
    {"revenue": 170, "value": 94.8, "company": "Company Q"},
    {"revenue": 180, "value": 93.9, "company": "Company R"},
    {"revenue": 190, "value": 94.3, "company": "Company S"},
    {"revenue": 200, "value": 93.5, "company": "Company T"},
]

client_tooltip_asset()
_PATH = rx.asset("scatter_chart.tsx", shared=True)


class ScatterChart(rx.NoSSRComponent):
    """Reflex wrapper around the parametrized ScatterChart TSX."""

    library = f"$/public{_PATH}"
    tag = "ScatterChart"
    is_default = False

    lib_dependencies: list[str] = ["d3"]

    data: rx.Var[list[ScatterPoint]] = rx.Var.create(_DEFAULT_DATA)
    color: rx.Var[str] = rx.Var.create("text-violet-400")


def scatter_chart(**props) -> rx.Component:
    """Scatter plot of ``{revenue, value, company}`` points with per-point tooltip.

    Args:
        data: list of ``{"revenue": x, "value": y, "company": label}``. Defaults to
            the original rosencharts example.
        color: Tailwind ``text-*`` class for the dots. Defaults to ``"text-violet-400"``.

    Returns:
        A Reflex component rendering the scatter chart.
    """
    return ScatterChart.create(**props)
