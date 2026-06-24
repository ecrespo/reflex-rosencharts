"""Thin horizontal bar chart (port of rosencharts
``bar-charts/6_BarChartThinHorizontal_DIV``).

The ``_DIV`` suffix in the original refers to the render technique (bars are
absolutely-positioned ``<div>``s, not SVG rects); it is dropped from the public
name. Thin bars with a rounded tip; bar color is chosen by magnitude. Sorted
descending by value internally. Data schema:
``list[{"key": str, "value": float}]``. Empty data renders an empty container.
"""

import reflex as rx

from ..helpers import client_tooltip as _client_tooltip  # noqa: F401

_path = rx.asset("./bar_chart_thin_horizontal.tsx", shared=True)


class BarChartThinHorizontal(rx.NoSSRComponent):
    """D3 + Tailwind thin horizontal bar chart. NoSSR (tooltip uses a DOM portal)."""

    library = f"$/public{_path}"
    tag = "BarChartThinHorizontal"
    is_default = False

    lib_dependencies: list[str] = ["d3@^7.9.0"]

    # data: list[{"key": str, "value": float}]
    data: rx.Var[list[dict]]


def bar_chart_thin_horizontal(**props) -> rx.Component:
    """Render a thin horizontal bar chart. Pass ``data=[{"key": ..., "value": ...}, ...]``."""
    return BarChartThinHorizontal.create(**props)
