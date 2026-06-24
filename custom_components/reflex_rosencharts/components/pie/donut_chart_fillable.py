"""Fillable full donut / gauge (port of rosencharts
``pie-charts/8_DonutChartFillable``).

This chart renders a single ``value`` in 0..100 as a filled donut rather than a
category list. The ``value`` prop sets the filled amount (default ``31``). With
no props the original rosencharts example is shown.
"""

import reflex as rx

_path = rx.asset("./donut_chart_fillable.tsx", shared=True)


class DonutChartFillable(rx.NoSSRComponent):
    """D3 + Tailwind fillable full-donut gauge for a single 0..100 value."""

    library = f"$/public{_path}"
    tag = "DonutChartFillable"
    is_default = False

    lib_dependencies: list[str] = ["d3@^7.9.0"]

    # value: float in 0..100 (filled amount)
    value: rx.Var[float]


def donut_chart_fillable(**props) -> rx.Component:
    """Render a fillable full-donut gauge. Pass ``value=<0..100>``."""
    return DonutChartFillable.create(**props)
