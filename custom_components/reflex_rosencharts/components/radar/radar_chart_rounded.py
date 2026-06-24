"""Rounded radar chart wrapper (port of rosencharts ``radar-charts/8_RadarChartRounded``).

Data schema: ``list[{"topic": str, "value": float}]``. Same shape as the plain
radar chart, but the area is drawn with a closed cardinal curve and each data
point is marked with a labeled circle. Empty data renders an empty container.
With no ``data`` the original rosencharts example dataset is shown.
"""

import reflex as rx

_path = rx.asset("./radar_chart_rounded.tsx", shared=True)


class RadarChartRounded(rx.NoSSRComponent):
    """D3 + Tailwind rounded radar chart. NoSSR for consistent client-side rendering."""

    library = f"$/public{_path}"
    tag = "RadarChartRounded"
    is_default = False

    lib_dependencies: list[str] = ["d3@^7.9.0"]

    # data: list[{"topic": str, "value": float}]
    data: rx.Var[list[dict]]


def radar_chart_rounded(**props) -> rx.Component:
    """Render a rounded radar chart. Pass ``data=[{"topic": ..., "value": ...}, ...]``."""
    return RadarChartRounded.create(**props)
