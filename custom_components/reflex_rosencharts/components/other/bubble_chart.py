"""Bubble (circle pack) chart wrapper (port of rosencharts ``other-charts/4_BubbleChart_DIV``).

The ``_DIV`` suffix in the original refers to the render technique (each bubble
is an absolutely-positioned ``<div>`` circle, not an SVG ``<circle>``); it is
dropped from the public name. Data schema:
``list[{"name": str, "sector": str, "value": float}]``. Bubbles are sized with a
d3 circle-pack layout and colored by ``sector`` (palette cycled). Empty data
renders an empty container.
"""

import reflex as rx

_path = rx.asset("./bubble_chart.tsx", shared=True)


class BubbleChart(rx.NoSSRComponent):
    """D3 circle-pack + Tailwind bubble chart. NoSSR (client-only layout)."""

    library = f"$/public{_path}"
    tag = "BubbleChart"
    is_default = False

    lib_dependencies: list[str] = ["d3@^7.9.0"]

    # data: list[{"name": str, "sector": str, "value": float}]
    data: rx.Var[list[dict]]


def bubble_chart(**props) -> rx.Component:
    """Render a bubble chart. Pass ``data=[{"name": ..., "sector": ..., "value": ...}, ...]``."""
    return BubbleChart.create(**props)
