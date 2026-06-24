"""Half donut chart (port of rosencharts ``pie-charts/6_DonutChartHalf``).

Data schema: ``list[{"name": str, "value": float}]``. Slice colors cycle
through a fixed palette so any number of slices renders. Empty data renders an
empty container. With no ``data`` the original rosencharts example dataset is
shown.
"""

import reflex as rx

_path = rx.asset("./donut_chart_half.tsx", shared=True)


class DonutChartHalf(rx.NoSSRComponent):
    """D3 + Tailwind half (semi-circle) donut chart."""

    library = f"$/public{_path}"
    tag = "DonutChartHalf"
    is_default = False

    lib_dependencies: list[str] = ["d3@^7.9.0"]

    # data: list[{"name": str, "value": float}]
    data: rx.Var[list[dict]]


def donut_chart_half(**props) -> rx.Component:
    """Render a half donut chart. Pass ``data=[{"name": ..., "value": ...}, ...]``."""
    return DonutChartHalf.create(**props)
