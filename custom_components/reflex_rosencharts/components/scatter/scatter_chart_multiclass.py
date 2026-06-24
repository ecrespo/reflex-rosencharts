"""Multiclass scatter chart wrapper (port of rosencharts
``scatter-charts/5_ScatterChartMulticlass``).

Data schema: ``list[{"revenue": float, "value": float, "company": str,
"category": str}]``. ``revenue`` is the x value, ``value`` is the y value,
``company`` labels the tooltip, and ``category`` groups points into color
classes (cycled through a fixed palette). Empty data renders an empty container
of the same size. With no ``data`` the original rosencharts example (two
classes merged) is shown.
"""

import reflex as rx

from ..helpers import client_tooltip as _client_tooltip  # noqa: F401

_path = rx.asset("./scatter_chart_multiclass.tsx", shared=True)


class ScatterChartMulticlass(rx.NoSSRComponent):
    """D3 + Tailwind multiclass scatter chart. NoSSR because the tooltip uses a DOM portal."""

    library = f"$/public{_path}"
    tag = "ScatterChartMulticlass"
    is_default = False

    lib_dependencies: list[str] = ["d3@^7.9.0"]

    # data: list[{"revenue": float, "value": float, "company": str, "category": str}]
    data: rx.Var[list[dict]]


def scatter_chart_multiclass(**props) -> rx.Component:
    """Render a multiclass scatter chart.

    Pass ``data=[{"revenue": ..., "value": ..., "company": ..., "category": ...}, ...]``.
    Points are colored by ``category``.
    """
    return ScatterChartMulticlass.create(**props)
