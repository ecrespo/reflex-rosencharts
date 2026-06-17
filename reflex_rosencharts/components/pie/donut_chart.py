"""donut_chart — port of rosencharts pie-charts/4_DonutChart.tsx to Reflex.

Render technique: D3 ``pie``/``arc`` donut slices with a clip-path + linear-gradient
3D light effect and inline SVG text labels. Uses the shared ClientTooltip helper
(createPortal), so the component is client-side only (NoSSRComponent).

Data schema (``CategoryValue``)::

    {"name": str, "value": float}

Example::

    import reflex_rosencharts as rxc
    rxc.donut_chart(data=[{"name": "AAPL", "value": 30}], colors=["#7e4cfe"])
"""

from typing import TypedDict

import reflex as rx

from ..helpers.client_tooltip import client_tooltip_asset


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

client_tooltip_asset()
_PATH = rx.asset("donut_chart.tsx", shared=True)


class DonutChart(rx.NoSSRComponent):
    """Reflex wrapper around the parametrized DonutChart TSX."""

    library = f"$/public{_PATH}"
    tag = "DonutChart"
    is_default = False

    lib_dependencies: list[str] = ["d3"]

    data: rx.Var[list[CategoryValue]] = rx.Var.create(_DEFAULT_DATA)
    colors: rx.Var[list[str]] = rx.Var.create(_DEFAULT_COLORS)


def donut_chart(**props) -> rx.Component:
    """Donut chart with a 3D light effect and a per-slice tooltip.

    Args:
        data: list of ``{"name": str, "value": float}``. Defaults to the original
            rosencharts example.
        colors: palette (hex strings) cycled across slices.

    Returns:
        A Reflex component rendering the donut chart.
    """
    return DonutChart.create(**props)
