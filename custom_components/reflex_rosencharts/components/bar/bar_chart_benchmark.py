"""Benchmark bar chart (port of rosencharts ``bar-charts/15_BarChartBenchmark``).

A vertical stack of labeled progress-style bars where each bar's fill is scaled
relative to the maximum value; the first row (index 0) is highlighted as the
benchmark. Data schema: ``list[{"key": str, "value": float}]``. Empty data
renders an empty container.
"""

import reflex as rx

from ..helpers import client_tooltip as _client_tooltip  # noqa: F401

_path = rx.asset("./bar_chart_benchmark.tsx", shared=True)


class BarChartBenchmark(rx.NoSSRComponent):
    """Tailwind benchmark bar chart. NoSSR (tooltip uses a DOM portal)."""

    library = f"$/public{_path}"
    tag = "BarChartBenchmark"
    is_default = False

    lib_dependencies: list[str] = ["d3@^7.9.0"]

    # data: list[{"key": str, "value": float}]
    data: rx.Var[list[dict]]


def bar_chart_benchmark(**props) -> rx.Component:
    """Render a benchmark bar chart. Pass ``data=[{"key": ..., "value": ...}, ...]``."""
    return BarChartBenchmark.create(**props)
