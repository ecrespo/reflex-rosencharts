"""Line chart wrapper (port of rosencharts ``line-charts/1_LineChart``).

Data schema: ``list[{"date": str (YYYY-MM-DD), "value": float}]``. Empty data
renders an empty container (never raises). With no ``data`` the original
rosencharts example dataset is shown.
"""

import reflex as rx

from ..helpers import client_tooltip as _client_tooltip  # noqa: F401

_path = rx.asset("./line_chart.tsx", shared=True)


class LineChart(rx.NoSSRComponent):
    """D3 + Tailwind line chart. NoSSR because the tooltip uses a DOM portal."""

    library = f"$/public{_path}"
    tag = "LineChart"
    is_default = False

    lib_dependencies: list[str] = ["d3@^7.9.0"]

    # data: list[{"date": str, "value": float}]
    data: rx.Var[list[dict]]


def line_chart(**props) -> rx.Component:
    """Render a line chart. Pass ``data=[{"date": ..., "value": ...}, ...]``."""
    return LineChart.create(**props)
