"""Pulse line chart wrapper (port of rosencharts ``line-charts/7_LineChartPulse``).

Data schema: ``list[{"date": str (YYYY-MM-DD), "value": float}]``. The latest
point gets an animated pulsing dot. Empty data renders an empty container (never
raises). With no ``data`` the original rosencharts example dataset is shown.

Since 0.2.2 the y-axis gutter is sized from the longest label instead of a fixed
25px, so 3+ digit values no longer wrap; override it with ``margin_left``.

Since 0.2.4 the x-axis labels never overlap: labels that do not fit the measured
width are dropped (first point > last point > maximum). ``x_ticks="regular"``
switches to evenly spaced date ticks.
"""

import reflex as rx

from ..helpers import chart_axis as _chart_axis  # noqa: F401
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

    # x axis labels: "extremes" (default: first, last and maximum point) or
    # "regular" (evenly spaced date ticks). Labels that would overlap are dropped.
    x_ticks: rx.Var[str]

    # Width of the y-axis gutter ("46px" or 46). Defaults to a value computed
    # from the longest y label, so 3+ digit values never wrap onto two lines.
    margin_left: rx.Var[str | int]


def line_chart_pulse(**props) -> rx.Component:
    """Render a pulse line chart. Pass ``data=[{"date": ..., "value": ...}, ...]``."""
    return LineChartPulse.create(**props)
