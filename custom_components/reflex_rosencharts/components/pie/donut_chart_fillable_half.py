"""Fillable half donut / gauge (port of rosencharts
``pie-charts/7_DonutChartFillableHalf``).

This chart renders a single ``value`` in 0..100 as a filled gauge rather than a
category list. The ``value`` prop sets the filled percentage (default ``31``).
With no props the original rosencharts example is shown.
"""

import reflex as rx

_path = rx.asset("./donut_chart_fillable_half.tsx", shared=True)


class DonutChartFillableHalf(rx.NoSSRComponent):
    """D3 + Tailwind fillable half-donut gauge for a single 0..100 value."""

    library = f"$/public{_path}"
    tag = "DonutChartFillableHalf"
    is_default = False

    lib_dependencies: list[str] = ["d3@^7.9.0"]

    # value: float in 0..100 (filled percentage)
    value: rx.Var[float]


def donut_chart_fillable_half(**props) -> rx.Component:
    """Render a fillable half-donut gauge. Pass ``value=<0..100>``."""
    return DonutChartFillableHalf.create(**props)
