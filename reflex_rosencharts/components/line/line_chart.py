"""line_chart — port of rosencharts line-charts/1_LineChart.tsx to Reflex.

Render technique: SVG path computed with D3 (scaleTime/scaleLinear/d3.line),
styled with Tailwind. Uses the shared ClientTooltip helper (createPortal), so the
component is rendered client-side only (NoSSRComponent).

Data schema (``LinePoint``)::

    {"date": "YYYY-MM-DD", "value": float}

Example::

    import reflex_rosencharts as rxc
    rxc.line_chart(data=State.sales, color="stroke-indigo-500")
"""

from typing import TypedDict

import reflex as rx

from ..helpers.client_tooltip import client_tooltip_asset


class LinePoint(TypedDict):
    """A single point of a time series."""

    date: str  # ISO date 'YYYY-MM-DD'
    value: float


# Default dataset == the original rosencharts example, so ``line_chart()`` with no
# args reproduces the reference chart (Tech Design DD-002).
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

# Ship the shared helper next to this chart so the TSX's ``../helpers/ClientTooltip``
# relative import resolves in the generated frontend.
client_tooltip_asset()
_PATH = rx.asset("line_chart.tsx", shared=True)


class LineChart(rx.NoSSRComponent):
    """Reflex wrapper around the parametrized LineChart TSX."""

    library = f"$/public{_PATH}"
    tag = "LineChart"
    is_default = False

    lib_dependencies: list[str] = ["d3"]

    # Props
    data: rx.Var[list[LinePoint]] = rx.Var.create(_DEFAULT_DATA)
    color: rx.Var[str] = rx.Var.create("stroke-fuchsia-400")


def line_chart(**props) -> rx.Component:
    """Time-series line chart with a per-point tooltip.

    Args:
        data: list of ``{"date": "YYYY-MM-DD", "value": float}``. Defaults to the
            original rosencharts example.
        color: Tailwind ``stroke-*`` class for the line. Defaults to
            ``"stroke-fuchsia-400"``.

    Returns:
        A Reflex component rendering the line chart.
    """
    return LineChart.create(**props)
