"""pie_chart_labels — port of rosencharts pie-charts/3_PieChartLabels.tsx to Reflex.

Render technique: D3 ``pie``/``arc`` slices filled with per-slice linear gradients
(Tailwind ``text-*`` classes drive the gradient stops), with name + value labels as
absolutely positioned divs. Uses the shared ClientTooltip helper (createPortal), so
the component is client-side only (NoSSRComponent).

Data schema (``GradientSlice``)::

    {"name": str, "value": float, "colorFrom": str, "colorTo": str}

``colorFrom``/``colorTo`` are Tailwind ``text-*`` classes for the gradient stops.

Example::

    import reflex_rosencharts as rxc
    rxc.pie_chart_labels(data=State.sectors)
"""

from typing import TypedDict

import reflex as rx

from ..helpers.client_tooltip import client_tooltip_asset


class GradientSlice(TypedDict):
    """A pie slice with a per-slice Tailwind gradient."""

    name: str
    value: float
    colorFrom: str  # Tailwind text-* class
    colorTo: str  # Tailwind text-* class


_DEFAULT_DATA: list[GradientSlice] = [
    {"name": "Technology", "value": 731, "colorFrom": "text-pink-400", "colorTo": "text-pink-400"},
    {
        "name": "Industrials",
        "value": 631,
        "colorFrom": "text-purple-400",
        "colorTo": "text-purple-400",
    },
    {"name": "Cyclical", "value": 331, "colorFrom": "text-indigo-400", "colorTo": "text-indigo-400"},
    {"name": "Energy", "value": 232, "colorFrom": "text-sky-400", "colorTo": "text-sky-400"},
    {"name": "Defensive", "value": 101, "colorFrom": "text-lime-400", "colorTo": "text-lime-400"},
    {"name": "Financials", "value": 42, "colorFrom": "text-amber-400", "colorTo": "text-amber-400"},
]

client_tooltip_asset()
_PATH = rx.asset("pie_chart_labels.tsx", shared=True)


class PieChartLabels(rx.NoSSRComponent):
    """Reflex wrapper around the parametrized PieChartLabels TSX."""

    library = f"$/public{_PATH}"
    tag = "PieChartLabels"
    is_default = False

    lib_dependencies: list[str] = ["d3"]

    data: rx.Var[list[GradientSlice]] = rx.Var.create(_DEFAULT_DATA)


def pie_chart_labels(**props) -> rx.Component:
    """Pie chart with gradient slices plus name and value labels.

    Args:
        data: list of ``{"name", "value", "colorFrom", "colorTo"}`` where the colour
            fields are Tailwind ``text-*`` classes. Defaults to the original example.

    Returns:
        A Reflex component rendering the labelled pie chart.
    """
    return PieChartLabels.create(**props)
