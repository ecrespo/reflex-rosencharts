"""Thin stacked breakdown bar chart (port of rosencharts
``bar-charts/5_BarChartThinBreakdown``).

A single thin horizontal bar split into proportional segments, with each key
labeled below its segment. Each item carries a Tailwind gradient ``color``
(``from-*`` / ``to-*``). Data schema:
``list[{"key": str, "value": float, "color": str}]``. Empty data renders an
empty container.
"""

import reflex as rx

_path = rx.asset("./bar_chart_thin_breakdown.tsx", shared=True)


class BarChartThinBreakdown(rx.NoSSRComponent):
    """Tailwind thin stacked breakdown bar chart."""

    library = f"$/public{_path}"
    tag = "BarChartThinBreakdown"
    is_default = False

    lib_dependencies: list[str] = ["d3@^7.9.0"]

    # data: list[{"key": str, "value": float, "color": str}]
    data: rx.Var[list[dict]]


def bar_chart_thin_breakdown(**props) -> rx.Component:
    """Render a thin stacked breakdown bar chart. Pass ``data=[{"key", "value", "color"}, ...]``."""
    return BarChartThinBreakdown.create(**props)
