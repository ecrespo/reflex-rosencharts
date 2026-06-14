"""donut_chart_half — port of rosencharts pie-charts/6_DonutChartHalf.tsx to Reflex.

Render technique: D3 ``pie``/``arc`` constrained to a half circle (start ``-π/2``,
end ``π/2``) with a clip-path + linear-gradient 3D light effect and inline SVG text
labels. This chart does NOT use a tooltip, so it subclasses ``rx.Component``.

Data schema (``CategoryValue``)::

    {"name": str, "value": float}

Example::

    import reflex_rosencharts as rxc
    rxc.donut_chart_half(data=State.alloc, colors=["#7e4cfe"])
"""

from typing import TypedDict

import reflex as rx


class CategoryValue(TypedDict):
    """A single category/value slice."""

    name: str
    value: float


_DEFAULT_DATA: list[CategoryValue] = [
    {"name": "AAPL", "value": 30},
    {"name": "BTC", "value": 22},
    {"name": "GOLD", "value": 11},
    {"name": "PLTR", "value": 9},
    {"name": "ADA", "value": 7},
    {"name": "MSFT", "value": 3},
]

_DEFAULT_COLORS: list[str] = ["#7e4cfe", "#895cfc", "#956bff", "#a37fff", "#b291fd", "#b597ff"]

_PATH = rx.asset("donut_chart_half.tsx", shared=True)


class DonutChartHalf(rx.Component):
    """Reflex wrapper around the parametrized DonutChartHalf TSX."""

    library = f"$/public{_PATH}"
    tag = "DonutChartHalf"
    is_default = False

    lib_dependencies: list[str] = ["d3"]

    data: rx.Var[list[CategoryValue]] = rx.Var.create(_DEFAULT_DATA)
    colors: rx.Var[list[str]] = rx.Var.create(_DEFAULT_COLORS)


def donut_chart_half(**props) -> rx.Component:
    """Half-donut chart with a 3D light effect and inline labels (no tooltip).

    Args:
        data: list of ``{"name": str, "value": float}``. Defaults to the original
            rosencharts example.
        colors: palette (hex strings) cycled across slices.

    Returns:
        A Reflex component rendering the half-donut chart.
    """
    return DonutChartHalf.create(**props)
