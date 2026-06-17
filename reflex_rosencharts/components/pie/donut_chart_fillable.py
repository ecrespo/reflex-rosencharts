"""donut_chart_fillable — port of rosencharts pie-charts/8_DonutChartFillable.tsx.

Render technique: a two-slice full donut (filled vs empty) used as a progress ring.
The fill is driven by a single ``value`` prop in the 0-100 range (the TSX clamps it),
with a centered ``value / 100`` overlay div. No tooltip → ``rx.Component``.

Props: ``value`` (0-100 fill percent) and ``label`` (caption above the value).

Example::

    import reflex_rosencharts as rxc
    rxc.donut_chart_fillable(value=72, label="Filled")
"""

import reflex as rx

_PATH = rx.asset("donut_chart_fillable.tsx", shared=True)


class DonutChartFillable(rx.Component):
    """Reflex wrapper around the parametrized DonutChartFillable TSX."""

    library = f"$/public{_PATH}"
    tag = "DonutChartFillable"
    is_default = False

    lib_dependencies: list[str] = ["d3"]

    value: rx.Var[float] = rx.Var.create(31)
    label: rx.Var[str] = rx.Var.create("Filled")


def donut_chart_fillable(**props) -> rx.Component:
    """Full-donut progress ring filled to a 0-100 ``value`` (no tooltip).

    Args:
        value: fill percentage in ``[0, 100]`` (clamped client-side). Default ``31``.
        label: caption shown above the ``value / 100`` overlay. Default ``"Filled"``.

    Returns:
        A Reflex component rendering the fillable donut progress ring.
    """
    return DonutChartFillable.create(**props)
