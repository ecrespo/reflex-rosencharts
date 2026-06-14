"""donut_chart_center_text — port of rosencharts pie-charts/5_DonutChartCenterText.tsx.

Render technique: same donut as :func:`donut_chart` (D3 ``pie``/``arc`` with clip-path
gradient light effect) plus a centered overlay div showing a label and a total. Uses
the shared ClientTooltip helper (createPortal), so the component is client-side only
(NoSSRComponent).

Data schema (``CategoryValue``)::

    {"name": str, "value": float}

Extra props: ``center_label`` (small caption) and ``center_text`` (large value).

Example::

    import reflex_rosencharts as rxc
    rxc.donut_chart_center_text(data=State.alloc, center_text="184")
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
_PATH = rx.asset("donut_chart_center_text.tsx", shared=True)


class DonutChartCenterText(rx.NoSSRComponent):
    """Reflex wrapper around the parametrized DonutChartCenterText TSX."""

    library = f"$/public{_PATH}"
    tag = "DonutChartCenterText"
    is_default = False

    lib_dependencies: list[str] = ["d3"]

    data: rx.Var[list[CategoryValue]] = rx.Var.create(_DEFAULT_DATA)
    colors: rx.Var[list[str]] = rx.Var.create(_DEFAULT_COLORS)
    center_label: rx.Var[str] = rx.Var.create("Total")
    center_text: rx.Var[str] = rx.Var.create("184")


def donut_chart_center_text(**props) -> rx.Component:
    """Donut chart with a centered label/value overlay and a per-slice tooltip.

    Args:
        data: list of ``{"name": str, "value": float}``. Defaults to the original
            rosencharts example.
        colors: palette (hex strings) cycled across slices.
        center_label: small caption above the centered value (default ``"Total"``).
        center_text: large centered value (default ``"184"``).

    Returns:
        A Reflex component rendering the donut chart with center text.
    """
    return DonutChartCenterText.create(**props)
