"""Horizontal bar chart with company logos (port of rosencharts
``bar-charts/2_BarChartHorizontalLogo_DIV``).

The ``_DIV`` suffix in the original refers to the render technique (bars are
absolutely-positioned ``<div>``s, not SVG rects); it is dropped from the public
name. Each item carries its own Tailwind ``color`` class; circular company logos
are rendered per row from a built-in SVG set (indexed modulo). Data schema:
``list[{"key": str, "value": float, "color": str}]``. Empty data renders an
empty container.
"""

import reflex as rx

from ..helpers import client_tooltip as _client_tooltip  # noqa: F401

_path = rx.asset("./bar_chart_horizontal_logo.tsx", shared=True)


class BarChartHorizontalLogo(rx.NoSSRComponent):
    """D3 + Tailwind horizontal bar chart with logos. NoSSR (tooltip uses a DOM portal)."""

    library = f"$/public{_path}"
    tag = "BarChartHorizontalLogo"
    is_default = False

    lib_dependencies: list[str] = ["d3@^7.9.0"]

    # data: list[{"key": str, "value": float, "color": str}]
    data: rx.Var[list[dict]]


def bar_chart_horizontal_logo(**props) -> rx.Component:
    """Render a horizontal bar chart with logos. Pass ``data=[{"key", "value", "color"}, ...]``."""
    return BarChartHorizontalLogo.create(**props)
