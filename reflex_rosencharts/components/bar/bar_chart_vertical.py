"""bar_chart_vertical — port of rosencharts bar-charts/9_BarChartVertical_DIV.tsx.

Render technique: DIV-based vertical bars with D3 scales; pads to a minimum of 10
bars with empty placeholders so small datasets still look balanced. No tooltip, so
this subclasses ``rx.Component`` (not NoSSR). The ``_DIV`` suffix is dropped (render
technique only).

Data schema (``BarItem``)::

    {"key": str, "value": float}

Example::

    import reflex_rosencharts as rxc
    rxc.bar_chart_vertical(data=State.sectors)
"""

from typing import TypedDict

import reflex as rx


class BarItem(TypedDict):
    """A single bar: a category key and its value."""

    key: str
    value: float


_DEFAULT_DATA: list[BarItem] = [
    {"key": "Technology", "value": 18.1},
    {"key": "Utilities", "value": 14.3},
    {"key": "Energy", "value": 27.1},
    {"key": "Cyclicals", "value": 40},
    {"key": "Defensive", "value": 12.7},
    {"key": "Financials", "value": 22.8},
    {"key": "Health", "value": 17.8},
    {"key": "Real Estate", "value": 5.8},
    {"key": "Communications", "value": 42},
    {"key": "Materials", "value": 12.7},
    {"key": "Whatever", "value": 24.7},
    {"key": "Whenever", "value": 19.7},
    {"key": "Whomever", "value": 29.7},
]

_PATH = rx.asset("bar_chart_vertical.tsx", shared=True)


class BarChartVertical(rx.Component):
    """Reflex wrapper around the parametrized BarChartVertical TSX."""

    library = f"$/public{_PATH}"
    tag = "BarChartVertical"
    is_default = False

    lib_dependencies: list[str] = ["d3"]

    data: rx.Var[list[BarItem]] = rx.Var.create(_DEFAULT_DATA)


def bar_chart_vertical(**props) -> rx.Component:
    """Vertical bar chart with rotated x-axis labels.

    Args:
        data: list of ``{"key": str, "value": float}``. Defaults to the original
            rosencharts example. Padded to a minimum of 10 bars.

    Returns:
        A Reflex component rendering the vertical bar chart.
    """
    return BarChartVertical.create(**props)
