"""bar_chart_benchmark — port of rosencharts bar-charts/15_BarChartBenchmark.tsx.

Render technique: DIV-based progress-style rows (label, a track bar filled
proportionally to the row's value vs the dataset max, and the value). The first row is
highlighted as the benchmark. No D3; uses the shared ClientTooltip helper, so it is
client-side only (NoSSRComponent).

Data schema (``BarItem``)::

    {"key": str, "value": float}

The first row (index 0) is styled as the benchmark.

Example::

    import reflex_rosencharts as rxc
    rxc.bar_chart_benchmark(data=State.models)
"""

from typing import TypedDict

import reflex as rx

from ..helpers.client_tooltip import client_tooltip_asset


class BarItem(TypedDict):
    """A single benchmark row: a key and its value."""

    key: str
    value: float


_DEFAULT_DATA: list[BarItem] = [
    {"key": "Model 0", "value": 85.8},
    {"key": "Model A", "value": 34.3},
    {"key": "Model B", "value": 27.1},
    {"key": "Model C", "value": 22.5},
]

client_tooltip_asset()
_PATH = rx.asset("bar_chart_benchmark.tsx", shared=True)


class BarChartBenchmark(rx.NoSSRComponent):
    """Reflex wrapper around the parametrized BarChartBenchmark TSX."""

    library = f"$/public{_PATH}"
    tag = "BarChartBenchmark"
    is_default = False

    data: rx.Var[list[BarItem]] = rx.Var.create(_DEFAULT_DATA)


def bar_chart_benchmark(**props) -> rx.Component:
    """Progress-style benchmark bars (first row highlighted) with a per-row tooltip.

    Args:
        data: list of ``{"key": str, "value": float}``. Defaults to the original
            rosencharts example. The first row is highlighted as the benchmark.

    Returns:
        A Reflex component rendering the benchmark bars.
    """
    return BarChartBenchmark.create(**props)
