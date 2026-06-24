"""Stacked breakdown bar chart (port of rosencharts
``bar-charts/4_BarChartBreakdown``).

A single thick horizontal bar split into proportional segments; each segment
shows its key and value centered. Each item carries a Tailwind gradient
``color`` (``from-*`` / ``to-*``). Data schema:
``list[{"key": str, "value": float, "color": str}]``. Empty data renders an
empty container.
"""

import reflex as rx

_path = rx.asset("./bar_chart_breakdown.tsx", shared=True)


class BarChartBreakdown(rx.NoSSRComponent):
    """Tailwind stacked breakdown bar chart."""

    library = f"$/public{_path}"
    tag = "BarChartBreakdown"
    is_default = False

    lib_dependencies: list[str] = ["d3@^7.9.0"]

    # data: list[{"key": str, "value": float, "color": str}]
    data: rx.Var[list[dict]]


def bar_chart_breakdown(**props) -> rx.Component:
    """Render a stacked breakdown bar chart. Pass ``data=[{"key", "value", "color"}, ...]``."""
    return BarChartBreakdown.create(**props)
