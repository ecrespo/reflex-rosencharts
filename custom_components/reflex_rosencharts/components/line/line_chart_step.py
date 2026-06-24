"""Step line chart wrapper (port of rosencharts ``line-charts/6_LineChartStep``).

Data schema: ``list[{"date": str (YYYY-MM-DD), "value": float}]``. Empty data
renders an empty container (never raises). With no ``data`` the original
rosencharts example dataset is shown.
"""

import reflex as rx

from ..helpers import client_tooltip as _client_tooltip  # noqa: F401

_path = rx.asset("./line_chart_step.tsx", shared=True)


class LineChartStep(rx.NoSSRComponent):
    """D3 + Tailwind step line chart. NoSSR because the tooltip uses a DOM portal."""

    library = f"$/public{_path}"
    tag = "LineChartStep"
    is_default = False

    lib_dependencies: list[str] = ["d3@^7.9.0"]

    # data: list[{"date": str, "value": float}]
    data: rx.Var[list[dict]]


def line_chart_step(**props) -> rx.Component:
    """Render a step line chart. Pass ``data=[{"date": ..., "value": ...}, ...]``."""
    return LineChartStep.create(**props)
