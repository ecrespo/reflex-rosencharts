"""Curved line chart with point labels (port of rosencharts ``line-charts/4_LineChartLabelsCurved``).

Data schema: ``list[{"date": str (YYYY-MM-DD), "value": float}]``. Empty data
renders an empty container (never raises). With no ``data`` the original
rosencharts example dataset is shown.

Since 0.2.4 the x-axis labels never overlap: labels that do not fit the measured
width are dropped (first point > last point > maximum). ``x_ticks="regular"``
switches to evenly spaced date ticks.
"""

import reflex as rx

from ..helpers import chart_axis as _chart_axis  # noqa: F401

_path = rx.asset("./line_chart_labels_curved.tsx", shared=True)


class LineChartLabelsCurved(rx.NoSSRComponent):
    """D3 + Tailwind curved line chart with value labels at each point."""

    library = f"$/public{_path}"
    tag = "LineChartLabelsCurved"
    is_default = False

    lib_dependencies: list[str] = ["d3@^7.9.0"]

    # data: list[{"date": str, "value": float}]
    data: rx.Var[list[dict]]

    # x axis labels: "extremes" (default: first, last and maximum point) or
    # "regular" (evenly spaced date ticks). Labels that would overlap are dropped.
    x_ticks: rx.Var[str]


def line_chart_labels_curved(**props) -> rx.Component:
    """Render a curved line chart with labels. Pass ``data=[{"date": ..., "value": ...}, ...]``."""
    return LineChartLabelsCurved.create(**props)
