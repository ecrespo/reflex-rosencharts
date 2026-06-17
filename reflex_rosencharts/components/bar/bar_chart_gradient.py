"""bar_chart_gradient — port of rosencharts bar-charts/3_BarChartGradient_DIV.tsx.

Render technique: DIV-based bars with D3 scales; each bar uses a Tailwind
``bg-gradient-to-b`` fill from the per-row ``color`` (``from-*`` / ``to-*`` classes).
Uses the shared ClientTooltip helper, so the component is client-side only
(NoSSRComponent). The ``_DIV`` suffix is dropped (render technique only).

Data schema (``GradientBarItem``)::

    {"key": str, "value": float, "color": str}  # color = Tailwind from-*/to-* classes

The chart sorts descending by value internally.

Example::

    import reflex_rosencharts as rxc
    rxc.bar_chart_gradient(data=State.sectors)
"""

from typing import TypedDict

import reflex as rx

from ..helpers.client_tooltip import client_tooltip_asset


class GradientBarItem(TypedDict):
    """A bar with a Tailwind gradient color spec."""

    key: str
    value: float
    color: str  # Tailwind 'from-* to-*' classes


_DEFAULT_DATA: list[GradientBarItem] = [
    {"key": "Technology", "value": 38.1, "color": "from-pink-300 to-pink-400"},
    {"key": "Financials", "value": 25.3, "color": "from-purple-300 to-purple-400"},
    {"key": "Energy", "value": 23.1, "color": "from-indigo-300 to-indigo-400"},
    {"key": "Cyclical", "value": 19.5, "color": "from-sky-300 to-sky-400"},
    {"key": "Defensive", "value": 14.7, "color": "from-orange-200 to-orange-300"},
    {"key": "Utilities", "value": 5.8, "color": "from-lime-300 to-lime-400"},
]

client_tooltip_asset()
_PATH = rx.asset("bar_chart_gradient.tsx", shared=True)


class BarChartGradient(rx.NoSSRComponent):
    """Reflex wrapper around the parametrized BarChartGradient TSX."""

    library = f"$/public{_PATH}"
    tag = "BarChartGradient"
    is_default = False

    lib_dependencies: list[str] = ["d3"]

    data: rx.Var[list[GradientBarItem]] = rx.Var.create(_DEFAULT_DATA)


def bar_chart_gradient(**props) -> rx.Component:
    """Horizontal gradient-filled bar chart with a per-bar tooltip.

    Args:
        data: list of ``{"key": str, "value": float, "color": str}``. Defaults to the
            original rosencharts example. Sorted descending by value internally.

    Returns:
        A Reflex component rendering the gradient bar chart.
    """
    return BarChartGradient.create(**props)
