"""Pie chart wrapper (port of rosencharts ``pie-charts/1_PieChart``).

Data schema: ``list[{"name": str, "value": float}]``. Slice colors cycle through
a fixed palette so any number of slices renders. Empty data renders an empty
container. With no ``data`` the original rosencharts example dataset is shown.
"""

import reflex as rx

from ..helpers import client_tooltip as _client_tooltip  # noqa: F401

_path = rx.asset("./pie_chart.tsx", shared=True)


class PieChart(rx.NoSSRComponent):
    """D3 + Tailwind pie chart. NoSSR because the tooltip uses a DOM portal."""

    library = f"$/public{_path}"
    tag = "PieChart"
    is_default = False

    lib_dependencies: list[str] = ["d3@^7.9.0"]

    # data: list[{"name": str, "value": float}]
    data: rx.Var[list[dict]]


def pie_chart(**props) -> rx.Component:
    """Render a pie chart. Pass ``data=[{"name": ..., "value": ...}, ...]``."""
    return PieChart.create(**props)
