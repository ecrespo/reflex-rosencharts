"""Donut chart with centered text (port of rosencharts
``pie-charts/5_DonutChartCenterText``).

Data schema: ``list[{"name": str, "value": float}]``. Slice colors cycle
through a fixed palette so any number of slices renders. The ``center_text``
prop sets the large value shown in the middle (default ``"184"``). Empty data
renders an empty container. With no ``data`` the original rosencharts example
dataset is shown.
"""

import reflex as rx

from ..helpers import client_tooltip as _client_tooltip  # noqa: F401

_path = rx.asset("./donut_chart_center_text.tsx", shared=True)


class DonutChartCenterText(rx.NoSSRComponent):
    """D3 + Tailwind donut chart with a centered total label."""

    library = f"$/public{_path}"
    tag = "DonutChartCenterText"
    is_default = False

    lib_dependencies: list[str] = ["d3@^7.9.0"]

    # data: list[{"name": str, "value": float}]
    data: rx.Var[list[dict]]
    # center_text -> centerText: text displayed in the donut center
    center_text: rx.Var[str]


def donut_chart_center_text(**props) -> rx.Component:
    """Render a donut chart with center text. Pass ``data=[...]`` and ``center_text="..."``."""
    return DonutChartCenterText.create(**props)
