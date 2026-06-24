"""Radar chart wrapper (port of rosencharts ``radar-charts/6_RadarChart``).

Data schema: ``list[{"topic": str, "value": float}]``. Each item is one axis of
the radar; the radial scale is computed from the maximum ``value``. Empty data
renders an empty container. With no ``data`` the original rosencharts example
dataset is shown.
"""

import reflex as rx

_path = rx.asset("./radar_chart.tsx", shared=True)


class RadarChart(rx.NoSSRComponent):
    """D3 + Tailwind radar chart. NoSSR for consistent client-side rendering."""

    library = f"$/public{_path}"
    tag = "RadarChart"
    is_default = False

    lib_dependencies: list[str] = ["d3@^7.9.0"]

    # data: list[{"topic": str, "value": float}]
    data: rx.Var[list[dict]]


def radar_chart(**props) -> rx.Component:
    """Render a radar chart. Pass ``data=[{"topic": ..., "value": ...}, ...]``."""
    return RadarChart.create(**props)
