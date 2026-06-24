"""Pie chart with in-slice labels and gradients (port of rosencharts
``pie-charts/3_PieChartLabels``).

Data schema: ``list[{"name": str, "value": float, "colorFrom": str, "colorTo": str}]``
where ``colorFrom``/``colorTo`` are Tailwind text-color classes used as the
slice gradient stops. Empty data renders an empty container. With no ``data``
the original rosencharts example dataset is shown.
"""

import reflex as rx

from ..helpers import client_tooltip as _client_tooltip  # noqa: F401

_path = rx.asset("./pie_chart_labels.tsx", shared=True)


class PieChartLabels(rx.NoSSRComponent):
    """D3 + Tailwind pie chart with gradient slices and centered labels."""

    library = f"$/public{_path}"
    tag = "PieChartLabels"
    is_default = False

    lib_dependencies: list[str] = ["d3@^7.9.0"]

    # data: list[{"name": str, "value": float, "colorFrom": str, "colorTo": str}]
    data: rx.Var[list[dict]]


def pie_chart_labels(**props) -> rx.Component:
    """Render a labeled pie chart. Pass ``data=[{"name", "value", "colorFrom", "colorTo"}, ...]``."""
    return PieChartLabels.create(**props)
