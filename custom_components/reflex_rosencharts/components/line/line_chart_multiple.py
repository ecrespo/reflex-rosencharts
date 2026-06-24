"""Multi-series line chart wrapper (port of rosencharts ``line-charts/3_LineChartMultiple``).

Data schema (both series): ``list[{"date": str (YYYY-MM-DD), "value": float}]``.
Empty ``data`` renders an empty container (never raises). With no ``data`` /
``data2`` the original rosencharts example datasets are shown.
"""

import reflex as rx

from ..helpers import client_tooltip as _client_tooltip  # noqa: F401

_path = rx.asset("./line_chart_multiple.tsx", shared=True)


class LineChartMultiple(rx.NoSSRComponent):
    """D3 + Tailwind multi-series line chart. NoSSR because the tooltip uses a DOM portal."""

    library = f"$/public{_path}"
    tag = "LineChartMultiple"
    is_default = False

    lib_dependencies: list[str] = ["d3@^7.9.0"]

    # data: list[{"date": str, "value": float}] (first series)
    data: rx.Var[list[dict]]
    # data2: list[{"date": str, "value": float}] (second series)
    data2: rx.Var[list[dict]]


def line_chart_multiple(**props) -> rx.Component:
    """Render a multi-series line chart.

    Pass ``data=[{"date": ..., "value": ...}, ...]`` and
    ``data2=[{"date": ..., "value": ...}, ...]``.
    """
    return LineChartMultiple.create(**props)
