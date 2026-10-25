"""Area chart wrapper (port of rosencharts ``area-charts/1_AreaChart``).

Data schema: ``list[{"date": str (YYYY-MM-DD), "value": float}]``. Empty data
renders an empty container (never raises). With no ``data`` the original
rosencharts example dataset is shown.

Since 0.2.4 the x-axis labels never overlap: labels that do not fit the measured
width are dropped (first point > last point > maximum). ``x_ticks="regular"``
switches to evenly spaced date ticks.
"""

import reflex as rx

# Importing this registers the shared ClientTooltip.tsx asset (symlink) that the
# chart TSX imports via the $/public alias.
from ..helpers import chart_axis as _chart_axis  # noqa: F401
from ..helpers import client_tooltip as _client_tooltip  # noqa: F401

# Copy the local TSX into the generated frontend and expose it as a component.
_path = rx.asset("./area_chart.tsx", shared=True)


class AreaChart(rx.NoSSRComponent):
    """D3 + Tailwind area chart. NoSSR because the tooltip uses a DOM portal."""

    library = f"$/public{_path}"
    tag = "AreaChart"
    is_default = False

    # The TSX imports from "d3"; ensure it is installed in the frontend.
    lib_dependencies: list[str] = ["d3@^7.9.0"]

    # data: list[{"date": str, "value": float}]
    data: rx.Var[list[dict]]

    # x axis labels: "extremes" (default: first, last and maximum point) or
    # "regular" (evenly spaced date ticks). Labels that would overlap are dropped.
    x_ticks: rx.Var[str]


def area_chart(**props) -> rx.Component:
    """Render an area chart. Pass ``data=[{"date": ..., "value": ...}, ...]``."""
    return AreaChart.create(**props)
