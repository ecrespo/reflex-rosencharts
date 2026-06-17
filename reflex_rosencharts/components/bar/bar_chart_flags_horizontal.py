"""bar_chart_flags_horizontal — port of bar-charts/7_BarChartFlagsHorizontal.tsx.

Render technique: DIV bars + D3 scales; each row shows a circular country flag
(loaded from hatscripts.github.io/circle-flags by the per-row ``flag`` code). No
tooltip, so this subclasses ``rx.Component`` (not NoSSR).

Data schema (``FlagBarItem``)::

    {"key": str, "value": float, "flag": str}  # flag = ISO 3166-1 alpha-2, e.g. "pt"

Example::

    import reflex_rosencharts as rxc
    rxc.bar_chart_flags_horizontal(data=State.countries)
"""

from typing import TypedDict

import reflex as rx


class FlagBarItem(TypedDict):
    """A bar with a country flag code."""

    key: str
    value: float
    flag: str  # ISO 3166-1 alpha-2 code (e.g. "pt", "fr")


_DEFAULT_DATA: list[FlagBarItem] = [
    {"key": "Portugal", "value": 55.8, "flag": "pt"},
    {"key": "France", "value": 34.3, "flag": "fr"},
    {"key": "Sweden", "value": 27.1, "flag": "se"},
    {"key": "Spain", "value": 22.5, "flag": "es"},
    {"key": "Italy", "value": 18.7, "flag": "it"},
    {"key": "Germany", "value": 10.8, "flag": "de"},
]

_PATH = rx.asset("bar_chart_flags_horizontal.tsx", shared=True)


class BarChartFlagsHorizontal(rx.Component):
    """Reflex wrapper around the parametrized BarChartFlagsHorizontal TSX."""

    library = f"$/public{_PATH}"
    tag = "BarChartFlagsHorizontal"
    is_default = False

    lib_dependencies: list[str] = ["d3"]

    data: rx.Var[list[FlagBarItem]] = rx.Var.create(_DEFAULT_DATA)


def bar_chart_flags_horizontal(**props) -> rx.Component:
    """Horizontal bar chart with per-row circular country flags.

    Args:
        data: list of ``{"key": str, "value": float, "flag": str}``. Defaults to the
            original rosencharts example. ``flag`` is an ISO 3166-1 alpha-2 code.

    Returns:
        A Reflex component rendering the flags horizontal bar chart.
    """
    return BarChartFlagsHorizontal.create(**props)
