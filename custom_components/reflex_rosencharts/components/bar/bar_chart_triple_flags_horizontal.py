"""Grouped horizontal bar chart with country flags (port of rosencharts
``bar-charts/12_BarChartTripleFlagsHorizontal_DIV``).

The ``_DIV`` suffix in the original refers to the render technique (bars are
absolutely-positioned ``<div>``s, not SVG rects); it is dropped from the public
name. Each category row is preceded by a circular country flag and renders one
horizontal bar per series value (three by default). Data schema:
``list[{"key": str, "values": list[float], "flag": str}]`` where ``flag`` is a
lowercase ISO 3166-1 alpha-2 code (e.g. ``"eu"``) and all items share the same
number of series. Empty data renders an empty container.
"""

import reflex as rx

from ..helpers import client_tooltip as _client_tooltip  # noqa: F401

_path = rx.asset("./bar_chart_triple_flags_horizontal.tsx", shared=True)


class BarChartTripleFlagsHorizontal(rx.NoSSRComponent):
    """D3 + Tailwind grouped horizontal bar chart with flags. NoSSR (tooltip uses a DOM portal)."""

    library = f"$/public{_path}"
    tag = "BarChartTripleFlagsHorizontal"
    is_default = False

    lib_dependencies: list[str] = ["d3@^7.9.0"]

    # data: list[{"key": str, "values": list[float], "flag": str}]
    data: rx.Var[list[dict]]


def bar_chart_triple_flags_horizontal(**props) -> rx.Component:
    """Render a grouped horizontal bar chart with flags. Pass ``data=[{"key", "values", "flag"}, ...]``."""
    return BarChartTripleFlagsHorizontal.create(**props)
