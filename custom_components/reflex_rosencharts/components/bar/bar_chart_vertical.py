"""Vertical bar chart (port of rosencharts ``bar-charts/9_BarChartVertical_DIV``).

The ``_DIV`` suffix in the original refers to the render technique (bars are
absolutely-positioned ``<div>``s, not SVG rects); it is dropped from the public
name. Pads the dataset with empty bars up to a minimum count so small datasets
still look balanced; x-axis labels are rotated 45deg. Data schema:
``list[{"key": str, "value": float}]``. Empty data renders an empty container.
"""

import reflex as rx

_path = rx.asset("./bar_chart_vertical.tsx", shared=True)


class BarChartVertical(rx.NoSSRComponent):
    """D3 + Tailwind vertical bar chart."""

    library = f"$/public{_path}"
    tag = "BarChartVertical"
    is_default = False

    lib_dependencies: list[str] = ["d3@^7.9.0"]

    # data: list[{"key": str, "value": float}]
    data: rx.Var[list[dict]]


def bar_chart_vertical(**props) -> rx.Component:
    """Render a vertical bar chart. Pass ``data=[{"key": ..., "value": ...}, ...]``."""
    return BarChartVertical.create(**props)
