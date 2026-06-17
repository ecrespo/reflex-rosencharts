"""line_chart_multiple — port of rosencharts line-charts/3_LineChartMultiple.tsx.

Render technique: two SVG paths (``curveMonotoneX``) over a shared set of D3
scales, styled with Tailwind. The first series carries the per-point tooltip
(shared ClientTooltip helper, createPortal) so the component is client-side only
(NoSSRComponent).

Data schema (``LinePoint``)::

    {"date": "YYYY-MM-DD", "value": float}

The two series are passed as ``data`` and ``data2``.

Example::

    import reflex_rosencharts as rxc
    rxc.line_chart_multiple(data=State.sales, data2=State.sales_prev)
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

_DEFAULT_DATA2: list[LinePoint] = [
    {"date": "2023-04-30", "value": 3},
    {"date": "2023-05-01", "value": 3.5},
    {"date": "2023-05-02", "value": 4},
    {"date": "2023-05-03", "value": 3.5},
    {"date": "2023-05-04", "value": 5},
    {"date": "2023-05-05", "value": 5},
    {"date": "2023-05-06", "value": 6},
    {"date": "2023-05-07", "value": 5.5},
    {"date": "2023-05-08", "value": 4},
    {"date": "2023-05-09", "value": 5},
]

client_tooltip_asset()
_PATH = rx.asset("line_chart_multiple.tsx", shared=True)


class LineChartMultiple(rx.NoSSRComponent):
    """Reflex wrapper around the parametrized LineChartMultiple TSX."""

    library = f"$/public{_PATH}"
    tag = "LineChartMultiple"
    is_default = False

    lib_dependencies: list[str] = ["d3"]

    data: rx.Var[list[LinePoint]] = rx.Var.create(_DEFAULT_DATA)
    data2: rx.Var[list[LinePoint]] = rx.Var.create(_DEFAULT_DATA2)
    color: rx.Var[str] = rx.Var.create("stroke-violet-400")
    color2: rx.Var[str] = rx.Var.create("stroke-fuchsia-400")


def line_chart_multiple(**props) -> rx.Component:
    """Two-series smooth line chart with a per-point tooltip on the first series.

    Args:
        data: primary series, list of ``{"date": "YYYY-MM-DD", "value": float}``.
        data2: secondary series, same schema.
        color: Tailwind ``stroke-*`` class for the primary line.
        color2: Tailwind ``stroke-*`` class for the secondary line.

    Returns:
        A Reflex component rendering the multi-series line chart.
    """
    return LineChartMultiple.create(**props)
