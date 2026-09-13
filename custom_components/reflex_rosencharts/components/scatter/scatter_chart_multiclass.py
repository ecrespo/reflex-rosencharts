"""Multiclass scatter chart wrapper (port of rosencharts
``scatter-charts/5_ScatterChartMulticlass``).

Data schema: ``list[{"revenue": float, "value": float, "company": str,
"category": str}]``. ``revenue`` is the x value, ``value`` is the y value,
``company`` labels the tooltip, and ``category`` groups points into color
classes (cycled through a fixed palette). Empty data renders an empty container
of the same size. With no ``data`` the original rosencharts example (two
classes merged) is shown.

Since 0.2.2 both axes are built from the *extent* of the data instead of its
first/last element, so the data no longer has to arrive sorted, the labels are
regular ticks that line up with the grid lines, and no point is clipped at the
edges of the plot.
"""

import reflex as rx

from ..helpers import chart_axis as _chart_axis  # noqa: F401
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

    # Width of the y-axis gutter ("46px" or 46). Defaults to a value computed
    # from the longest y label, so 3+ digit values never wrap onto two lines.
    margin_left: rx.Var[str | int]

    # X axis type: "linear" (default), "log" or "symlog".
    x_scale: rx.Var[str]

    # Y axis type: "linear" (default), "log" or "symlog".
    y_scale: rx.Var[str]


def scatter_chart_multiclass(**props) -> rx.Component:
    """Render a multiclass scatter chart.

    Pass ``data=[{"revenue": ..., "value": ..., "company": ..., "category": ...}, ...]``.
    Points are colored by ``category``.

    Optional props:
        margin_left: y-axis gutter width, e.g. ``"46px"`` or ``46``. By default
            it is derived from the longest y label.
        x_scale / y_scale: ``"linear"`` (default), ``"log"`` or ``"symlog"``.
            ``"log"`` needs strictly positive values and falls back to
            ``"symlog"`` when any value is <= 0.
    """
    return ScatterChartMulticlass.create(**props)
