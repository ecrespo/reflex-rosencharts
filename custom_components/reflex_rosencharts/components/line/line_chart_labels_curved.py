"""Curved line chart with point labels (port of rosencharts ``line-charts/4_LineChartLabelsCurved``).

Data schema: ``list[{"date": str (YYYY-MM-DD), "value": float}]``. Empty data
renders an empty container (never raises). With no ``data`` the original
rosencharts example dataset is shown.
"""

import reflex as rx

_path = rx.asset("./line_chart_labels_curved.tsx", shared=True)


class LineChartLabelsCurved(rx.NoSSRComponent):
    """D3 + Tailwind curved line chart with value labels at each point."""

    library = f"$/public{_path}"
    tag = "LineChartLabelsCurved"
    is_default = False

    lib_dependencies: list[str] = ["d3@^7.9.0"]

    # data: list[{"date": str, "value": float}]
    data: rx.Var[list[dict]]


def line_chart_labels_curved(**props) -> rx.Component:
    """Render a curved line chart with labels. Pass ``data=[{"date": ..., "value": ...}, ...]``."""
    return LineChartLabelsCurved.create(**props)
