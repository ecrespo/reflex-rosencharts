"""Pie chart with stock logos (port of rosencharts ``pie-charts/2_PieChartStocks``).

Data schema: ``list[{"name": str, "value": float, "logo": str, "color": str}]``
where ``logo`` is an image URL and ``color`` is a Tailwind text-color class
(e.g. ``"text-pink-400"``). Empty data renders an empty container. With no
``data`` the original rosencharts example dataset is shown.
"""

import reflex as rx

from ..helpers import client_tooltip as _client_tooltip  # noqa: F401

_path = rx.asset("./pie_chart_stocks.tsx", shared=True)


class PieChartStocks(rx.NoSSRComponent):
    """D3 + Tailwind pie chart with logos and connecting lines."""

    library = f"$/public{_path}"
    tag = "PieChartStocks"
    is_default = False

    lib_dependencies: list[str] = ["d3@^7.9.0"]

    # data: list[{"name": str, "value": float, "logo": str, "color": str}]
    data: rx.Var[list[dict]]


def pie_chart_stocks(**props) -> rx.Component:
    """Render a stocks pie chart. Pass ``data=[{"name", "value", "logo", "color"}, ...]``."""
    return PieChartStocks.create(**props)
