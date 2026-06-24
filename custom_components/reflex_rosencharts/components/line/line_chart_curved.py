"""Curved line chart wrapper (port of rosencharts ``line-charts/2_LineChartCurved``).

Data schema: ``list[{"date": str (YYYY-MM-DD), "value": float}]``. Empty data
renders an empty container (never raises). With no ``data`` the original
rosencharts example dataset is shown.
"""

import reflex as rx

from ..helpers import client_tooltip as _client_tooltip  # noqa: F401

_path = rx.asset("./line_chart_curved.tsx", shared=True)


class LineChartCurved(rx.NoSSRComponent):
    """D3 + Tailwind curved line chart. NoSSR because the tooltip uses a DOM portal."""

    library = f"$/public{_path}"
    tag = "LineChartCurved"
    is_default = False

    lib_dependencies: list[str] = ["d3@^7.9.0"]

    # data: list[{"date": str, "value": float}]
    data: rx.Var[list[dict]]


def line_chart_curved(**props) -> rx.Component:
    """Render a curved line chart. Pass ``data=[{"date": ..., "value": ...}, ...]``."""
    return LineChartCurved.create(**props)
