"""Grouped (multi-series) vertical bar chart (port of rosencharts
``bar-charts/11_BarChartMultiVertical_DIV``).

The ``_DIV`` suffix in the original refers to the render technique (bars are
absolutely-positioned ``<div>``s, not SVG rects); it is dropped from the public
name. Each category renders one bar per series value, grouped side by side;
x-axis labels are rotated 45deg. Data schema:
``list[{"key": str, "values": list[float]}]`` (all items share the same number
of series). Empty data renders an empty container.
"""

import reflex as rx

from ..helpers import client_tooltip as _client_tooltip  # noqa: F401

_path = rx.asset("./bar_chart_multi_vertical.tsx", shared=True)


class BarChartMultiVertical(rx.NoSSRComponent):
    """D3 + Tailwind grouped vertical bar chart. NoSSR (tooltip uses a DOM portal)."""

    library = f"$/public{_path}"
    tag = "BarChartMultiVertical"
    is_default = False

    lib_dependencies: list[str] = ["d3@^7.9.0"]

    # data: list[{"key": str, "values": list[float]}]
    data: rx.Var[list[dict]]


def bar_chart_multi_vertical(**props) -> rx.Component:
    """Render a grouped vertical bar chart. Pass ``data=[{"key": ..., "values": [...]}, ...]``."""
    return BarChartMultiVertical.create(**props)
