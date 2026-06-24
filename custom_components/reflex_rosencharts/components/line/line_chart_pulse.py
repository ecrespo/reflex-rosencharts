"""Pulse line chart wrapper (port of rosencharts ``line-charts/7_LineChartPulse``).

Data schema: ``list[{"date": str (YYYY-MM-DD), "value": float}]``. The latest
point gets an animated pulsing dot. Empty data renders an empty container (never
raises). With no ``data`` the original rosencharts example dataset is shown.
"""

import reflex as rx

from ..helpers import client_tooltip as _client_tooltip  # noqa: F401

_path = rx.asset("./line_chart_pulse.tsx", shared=True)


class LineChartPulse(rx.NoSSRComponent):
    """D3 + Tailwind line chart with a pulsing dot. NoSSR because the tooltip uses a DOM portal."""

    library = f"$/public{_path}"
    tag = "LineChartPulse"
    is_default = False

    lib_dependencies: list[str] = ["d3@^7.9.0"]

    # data: list[{"date": str, "value": float}]
    data: rx.Var[list[dict]]


def line_chart_pulse(**props) -> rx.Component:
    """Render a pulse line chart. Pass ``data=[{"date": ..., "value": ...}, ...]``."""
    return LineChartPulse.create(**props)
