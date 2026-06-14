"""scatter_chart_interactive — port of rosencharts scatter-charts/2_ScatterChartInteractive.tsx.

Render technique: SVG points (D3 ``scaleLinear`` on both axes) in a 0-100 viewBox,
styled with Tailwind. Uses the shared ClientTooltip helper (createPortal) → rendered
client-side only (NoSSRComponent). Each point emits ``on_point_click`` carrying the
clicked ``{revenue, value, company}`` dict.

Data schema (``ScatterPoint``)::

    {"revenue": float (x), "value": float (y), "company": str}

Example::

    import reflex_rosencharts as rxc
    rxc.scatter_chart_interactive(data=State.points, on_point_click=State.pick)
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
    {"revenue": 60, "value": 101.7, "company": "Company F"},
    {"revenue": 70, "value": 99.9, "company": "Company G"},
    {"revenue": 80, "value": 98.5, "company": "Company H"},
    {"revenue": 90, "value": 101.9, "company": "Company I"},
    {"revenue": 100, "value": 100.8, "company": "Company J"},
    {"revenue": 110, "value": 98.2, "company": "Company K"},
    {"revenue": 120, "value": 96.8, "company": "Company L"},
    {"revenue": 130, "value": 101.9, "company": "Company M"},
    {"revenue": 140, "value": 100.5, "company": "Company N"},
    {"revenue": 150, "value": 101.9, "company": "Company O"},
    {"revenue": 160, "value": 99.5, "company": "Company P"},
    {"revenue": 170, "value": 102.8, "company": "Company Q"},
    {"revenue": 180, "value": 98.9, "company": "Company R"},
]

client_tooltip_asset()
_PATH = rx.asset("scatter_chart_interactive.tsx", shared=True)


class ScatterChartInteractive(rx.NoSSRComponent):
    """Reflex wrapper around the parametrized ScatterChartInteractive TSX."""

    library = f"$/public{_PATH}"
    tag = "ScatterChartInteractive"
    is_default = False

    lib_dependencies: list[str] = ["d3"]

    data: rx.Var[list[ScatterPoint]] = rx.Var.create(_DEFAULT_DATA)
    color: rx.Var[str] = rx.Var.create("text-fuchsia-400")

    # Fires with the clicked point dict {revenue, value, company}.
    on_point_click: rx.EventHandler[rx.event.passthrough_event_spec(dict)]


def scatter_chart_interactive(**props) -> rx.Component:
    """Interactive scatter plot; each point emits ``on_point_click`` when clicked.

    Args:
        data: list of ``{"revenue": x, "value": y, "company": label}``. Defaults to
            the original rosencharts example.
        color: Tailwind ``text-*`` class for the dots. Defaults to ``"text-fuchsia-400"``.
        on_point_click: event handler receiving the clicked point dict.

    Returns:
        A Reflex component rendering the interactive scatter chart.
    """
    return ScatterChartInteractive.create(**props)
