"""Curved line chart with stock logos (port of rosencharts ``line-charts/5_LineChartStocksCurved``).

Data schema: ``list[{"date": str (YYYY-MM-DD), "value": float}]``. Each point is
decorated with a company logo cycled from a built-in palette. Empty data renders
an empty container (never raises). With no ``data`` the original rosencharts
example dataset is shown.

Since 0.2.2 the y-axis gutter is sized from the longest label instead of a fixed
25px, so 3+ digit values no longer wrap; override it with ``margin_left``.
"""

import reflex as rx

from ..helpers import chart_axis as _chart_axis  # noqa: F401

_path = rx.asset("./line_chart_stocks_curved.tsx", shared=True)


class LineChartStocksCurved(rx.NoSSRComponent):
    """D3 + Tailwind curved line chart with company-logo markers at each point."""

    library = f"$/public{_path}"
    tag = "LineChartStocksCurved"
    is_default = False

    lib_dependencies: list[str] = ["d3@^7.9.0"]

    # data: list[{"date": str, "value": float}]
    data: rx.Var[list[dict]]

    # Width of the y-axis gutter ("46px" or 46). Defaults to a value computed
    # from the longest y label, so 3+ digit values never wrap onto two lines.
    margin_left: rx.Var[str | int]


def line_chart_stocks_curved(**props) -> rx.Component:
    """Render a curved stocks line chart. Pass ``data=[{"date": ..., "value": ...}, ...]``."""
    return LineChartStocksCurved.create(**props)
