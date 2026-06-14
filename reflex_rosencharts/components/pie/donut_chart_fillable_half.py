"""donut_chart_fillable_half — port of rosencharts pie-charts/7_DonutChartFillableHalf.tsx.

Render technique: a two-slice half donut (filled vs empty) used as a gauge. The fill
is driven by a single ``value`` prop in the 0-100 range (the TSX clamps it). A
centered SVG label and percentage are drawn on top. No tooltip → ``rx.Component``.

Props: ``value`` (0-100 fill percent) and ``label`` (caption above the percentage).

Example::

    import reflex_rosencharts as rxc
    rxc.donut_chart_fillable_half(value=72, label="Goal")
"""

import reflex as rx

_PATH = rx.asset("donut_chart_fillable_half.tsx", shared=True)


class DonutChartFillableHalf(rx.Component):
    """Reflex wrapper around the parametrized DonutChartFillableHalf TSX."""

    library = f"$/public{_PATH}"
    tag = "DonutChartFillableHalf"
    is_default = False

    lib_dependencies: list[str] = ["d3"]

    value: rx.Var[float] = rx.Var.create(31)
    label: rx.Var[str] = rx.Var.create("Goal")


def donut_chart_fillable_half(**props) -> rx.Component:
    """Half-donut gauge filled to a 0-100 ``value`` (no tooltip).

    Args:
        value: fill percentage in ``[0, 100]`` (clamped client-side). Default ``31``.
        label: caption shown above the percentage. Default ``"Goal"``.

    Returns:
        A Reflex component rendering the fillable half-donut gauge.
    """
    return DonutChartFillableHalf.create(**props)
