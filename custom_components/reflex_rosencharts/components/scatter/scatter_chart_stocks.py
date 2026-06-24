"""Stocks scatter chart wrapper (port of rosencharts
``scatter-charts/6_ScatterChartStocks``).

Data schema: ``list[{"revenue": float, "value": float, "company": str}]``.
``revenue`` is the x value, ``value`` is the y value, ``company`` labels the
tooltip. Each point is rendered as a cycling inline company logo. Empty data
renders an empty container of the same size. With no ``data`` the original
rosencharts example dataset is shown.
"""

import reflex as rx

from ..helpers import client_tooltip as _client_tooltip  # noqa: F401

_path = rx.asset("./scatter_chart_stocks.tsx", shared=True)


class ScatterChartStocks(rx.NoSSRComponent):
    """D3 + Tailwind stocks scatter chart. NoSSR because the tooltip uses a DOM portal."""

    library = f"$/public{_path}"
    tag = "ScatterChartStocks"
    is_default = False

    lib_dependencies: list[str] = ["d3@^7.9.0"]

    # data: list[{"revenue": float, "value": float, "company": str}]
    data: rx.Var[list[dict]]


def scatter_chart_stocks(**props) -> rx.Component:
    """Render a stocks scatter chart (points shown as company logos).

    Pass ``data=[{"revenue": ..., "value": ..., "company": ...}, ...]``.
    """
    return ScatterChartStocks.create(**props)
