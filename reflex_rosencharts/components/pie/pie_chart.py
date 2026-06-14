"""pie_chart — port of rosencharts pie-charts/1_PieChart.tsx to Reflex.

Render technique: D3 ``pie``/``arc`` slices drawn as SVG paths, value labels as
absolutely positioned divs. Uses the shared ClientTooltip helper (createPortal),
so the component is client-side only (NoSSRComponent).

Data schema (``CategoryValue``)::

    {"name": str, "value": float}

Example::

    import reflex_rosencharts as rxc
    rxc.pie_chart(data=State.spending, colors=["#F5A5DB", "#B89DFB"])
"""

from typing import TypedDict

import reflex as rx

from ..helpers.client_tooltip import client_tooltip_asset


class CategoryValue(TypedDict):
    """A single category/value slice."""

    name: str
    value: float


_DEFAULT_DATA: list[CategoryValue] = [
    {"name": "Rent", "value": 731},
    {"name": "Food", "value": 631},
    {"name": "Household", "value": 331},
    {"name": "Transportation", "value": 232},
    {"name": "Entertainment", "value": 101},
    {"name": "Other", "value": 42},
]

_DEFAULT_COLORS: list[str] = [
    "#F5A5DB",
    "#B89DFB",
    "#758bcf",
    "#33C2EA",
    "#FFC182",
    "#73DC5A",
]

client_tooltip_asset()
_PATH = rx.asset("pie_chart.tsx", shared=True)


class PieChart(rx.NoSSRComponent):
    """Reflex wrapper around the parametrized PieChart TSX."""

    library = f"$/public{_PATH}"
    tag = "PieChart"
    is_default = False

    lib_dependencies: list[str] = ["d3"]

    data: rx.Var[list[CategoryValue]] = rx.Var.create(_DEFAULT_DATA)
    colors: rx.Var[list[str]] = rx.Var.create(_DEFAULT_COLORS)


def pie_chart(**props) -> rx.Component:
    """Pie chart with rounded gapped slices and a per-slice tooltip.

    Args:
        data: list of ``{"name": str, "value": float}``. Defaults to the original
            rosencharts example.
        colors: palette (hex strings) cycled across slices.

    Returns:
        A Reflex component rendering the pie chart.
    """
    return PieChart.create(**props)
