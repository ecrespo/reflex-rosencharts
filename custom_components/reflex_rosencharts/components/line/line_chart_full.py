"""Full-bleed line chart wrapper (port of rosencharts ``line-charts/8_LineChartFull``).

Data schema: ``list[{"date": str (YYYY-MM-DD), "value": float}]``. Axes are
overlaid inside the full-width chart area. Empty data renders an empty container
(never raises). With no ``data`` the original rosencharts example dataset is shown.
"""

import reflex as rx

_path = rx.asset("./line_chart_full.tsx", shared=True)


class LineChartFull(rx.NoSSRComponent):
    """D3 + Tailwind full-bleed line chart with overlaid axes."""

    library = f"$/public{_path}"
    tag = "LineChartFull"
    is_default = False

    lib_dependencies: list[str] = ["d3@^7.9.0"]

    # data: list[{"date": str, "value": float}]
    data: rx.Var[list[dict]]


def line_chart_full(**props) -> rx.Component:
    """Render a full-bleed line chart. Pass ``data=[{"date": ..., "value": ...}, ...]``."""
    return LineChartFull.create(**props)
