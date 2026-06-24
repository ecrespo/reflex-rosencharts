"""Horizontal bar chart wrapper (port of rosencharts ``bar-charts/1_BarChartHorizontal_DIV``).

The ``_DIV`` suffix in the original refers to the render technique (bars are
absolutely-positioned ``<div>``s, not SVG rects); it is dropped from the public
name. Data schema: ``list[{"key": str, "value": float}]`` (sorted descending by
value internally). Empty data renders an empty container.
"""

import reflex as rx

from ..helpers import client_tooltip as _client_tooltip  # noqa: F401

_path = rx.asset("./bar_chart_horizontal.tsx", shared=True)


class BarChartHorizontal(rx.NoSSRComponent):
    """D3 + Tailwind horizontal bar chart. NoSSR (tooltip uses a DOM portal)."""

    library = f"$/public{_path}"
    tag = "BarChartHorizontal"
    is_default = False

    lib_dependencies: list[str] = ["d3@^7.9.0"]

    # data: list[{"key": str, "value": float}]
    data: rx.Var[list[dict]]


def bar_chart_horizontal(**props) -> rx.Component:
    """Render a horizontal bar chart. Pass ``data=[{"key": ..., "value": ...}, ...]``."""
    return BarChartHorizontal.create(**props)
