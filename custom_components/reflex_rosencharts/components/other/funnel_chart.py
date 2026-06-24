"""Funnel chart wrapper (port of rosencharts ``other-charts/5_FunnelChart``).

Each datum is a funnel stage. Data schema:
``list[{"key": str, "value": float, "color": str}]`` where ``color`` is a
Tailwind gradient class string (e.g. ``"from-pink-300 to-pink-400 ..."``). Stages
are sorted descending by value internally and centered to form the funnel. Empty
data renders an empty container.
"""

import reflex as rx

_path = rx.asset("./funnel_chart.tsx", shared=True)


class FunnelChart(rx.NoSSRComponent):
    """Tailwind gradient funnel chart. NoSSR (client-only render)."""

    library = f"$/public{_path}"
    tag = "FunnelChart"
    is_default = False

    lib_dependencies: list[str] = ["d3@^7.9.0"]

    # data: list[{"key": str, "value": float, "color": str}]
    data: rx.Var[list[dict]]


def funnel_chart(**props) -> rx.Component:
    """Render a funnel chart. Pass ``data=[{"key": ..., "value": ..., "color": ...}, ...]``."""
    return FunnelChart.create(**props)
