"""Donut chart (port of rosencharts ``pie-charts/4_DonutChart``).

Data schema: ``list[{"name": str, "value": float}]``. Slice colors cycle
through a fixed palette so any number of slices renders. Empty data renders an
empty container. With no ``data`` the original rosencharts example dataset is
shown.
"""

import reflex as rx

from ..helpers import client_tooltip as _client_tooltip  # noqa: F401

_path = rx.asset("./donut_chart.tsx", shared=True)


class DonutChart(rx.NoSSRComponent):
    """D3 + Tailwind donut chart with 3D-effect slices and labels."""

    library = f"$/public{_path}"
    tag = "DonutChart"
    is_default = False

    lib_dependencies: list[str] = ["d3@^7.9.0"]

    # data: list[{"name": str, "value": float}]
    data: rx.Var[list[dict]]


def donut_chart(**props) -> rx.Component:
    """Render a donut chart. Pass ``data=[{"name": ..., "value": ...}, ...]``."""
    return DonutChart.create(**props)
