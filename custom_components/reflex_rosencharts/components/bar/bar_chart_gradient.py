"""Gradient horizontal bar chart (port of rosencharts
``bar-charts/3_BarChartGradient_DIV``).

The ``_DIV`` suffix in the original refers to the render technique (bars are
absolutely-positioned ``<div>``s, not SVG rects); it is dropped from the public
name. Each item carries a Tailwind gradient ``color`` (``from-*`` / ``to-*``).
Sorted descending by value internally. Data schema:
``list[{"key": str, "value": float, "color": str}]``. Empty data renders an
empty container.
"""

import reflex as rx

from ..helpers import client_tooltip as _client_tooltip  # noqa: F401

_path = rx.asset("./bar_chart_gradient.tsx", shared=True)


class BarChartGradient(rx.NoSSRComponent):
    """D3 + Tailwind gradient horizontal bar chart. NoSSR (tooltip uses a DOM portal)."""

    library = f"$/public{_path}"
    tag = "BarChartGradient"
    is_default = False

    lib_dependencies: list[str] = ["d3@^7.9.0"]

    # data: list[{"key": str, "value": float, "color": str}]
    data: rx.Var[list[dict]]


def bar_chart_gradient(**props) -> rx.Component:
    """Render a gradient horizontal bar chart. Pass ``data=[{"key", "value", "color"}, ...]``."""
    return BarChartGradient.create(**props)
