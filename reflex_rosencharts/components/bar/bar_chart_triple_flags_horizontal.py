"""bar_chart_triple_flags_horizontal — port of 12_BarChartTripleFlagsHorizontal_DIV.tsx.

Render technique: DIV grouped horizontal bars with D3 scales; each row shows a
circular country flag and a stack of value-proportional bars colored from the
``colors`` palette. Uses the shared ClientTooltip helper (client-side only,
NoSSRComponent). The ``_DIV`` suffix is dropped (render technique only).

Data schema (``TripleFlagItem``)::

    {"key": str, "values": list[float], "flag": str}  # flag = ISO 3166 alpha-2

Example::

    import reflex_rosencharts as rxc
    rxc.bar_chart_triple_flags_horizontal(data=State.regions)
"""

from typing import TypedDict

import reflex as rx

from ..helpers.client_tooltip import client_tooltip_asset


class TripleFlagItem(TypedDict):
    """A grouped horizontal bar with a flag code."""

    key: str
    values: list[float]
    flag: str  # ISO 3166-1 alpha-2 code (e.g. "eu", "us")


_DEFAULT_DATA: list[TripleFlagItem] = [
    {"key": "European Union", "values": [15, 25, 33], "flag": "eu"},
    {"key": "United States", "values": [11, 22, 29], "flag": "us"},
    {"key": "China", "values": [5, 16, 21], "flag": "cn"},
    {"key": "Philippines", "values": [4, 11, 19], "flag": "ph"},
]
_DEFAULT_COLORS: list[str] = ["#F8ED53", "#E7E7F5", "#EEBA6B"]

client_tooltip_asset()
_PATH = rx.asset("bar_chart_triple_flags_horizontal.tsx", shared=True)


class BarChartTripleFlagsHorizontal(rx.NoSSRComponent):
    """Reflex wrapper around the parametrized BarChartTripleFlagsHorizontal TSX."""

    library = f"$/public{_PATH}"
    tag = "BarChartTripleFlagsHorizontal"
    is_default = False

    lib_dependencies: list[str] = ["d3"]

    data: rx.Var[list[TripleFlagItem]] = rx.Var.create(_DEFAULT_DATA)
    colors: rx.Var[list[str]] = rx.Var.create(_DEFAULT_COLORS)


def bar_chart_triple_flags_horizontal(**props) -> rx.Component:
    """Grouped horizontal bar chart with per-row flags and a tooltip.

    Args:
        data: list of ``{"key": str, "values": list[float], "flag": str}``. Defaults
            to the original rosencharts example. ``flag`` is an ISO 3166-1 alpha-2 code.
        colors: palette (CSS colors) for the bars within each group. Defaults to
            ``["#F8ED53", "#E7E7F5", "#EEBA6B"]``.

    Returns:
        A Reflex component rendering the triple-flags horizontal bar chart.
    """
    return BarChartTripleFlagsHorizontal.create(**props)
