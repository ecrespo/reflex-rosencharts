"""bar_chart_multi_vertical — port of bar-charts/11_BarChartMultiVertical_DIV.tsx.

Render technique: DIV-based grouped vertical bars with D3 scales; each category holds
a list of values rendered as adjacent bars colored from the ``colors`` palette. Uses
the shared ClientTooltip helper (client-side only, NoSSRComponent). The ``_DIV``
suffix is dropped (render technique only).

Data schema (``MultiBarItem``)::

    {"key": str, "values": list[float]}

Example::

    import reflex_rosencharts as rxc
    rxc.bar_chart_multi_vertical(
        data=State.months, colors=["#B89DFB", "#e7deff"]
    )
"""

from typing import TypedDict

import reflex as rx

from ..helpers.client_tooltip import client_tooltip_asset


class MultiBarItem(TypedDict):
    """A grouped bar: a category key and a list of values."""

    key: str
    values: list[float]


_DEFAULT_DATA: list[MultiBarItem] = [
    {"key": "Jan 2020", "values": [11.1, 9.5]},
    {"key": "Feb 2020", "values": [18.3, 16.7]},
    {"key": "Mar 2020", "values": [25.1, 19.5]},
    {"key": "Apr 2020", "values": [35.5, 24.9]},
    {"key": "May 2020", "values": [31.7, 28.1]},
    {"key": "Jun 2020", "values": [25.8, 20.2]},
    {"key": "Jul 2020", "values": [15.8, 10.2]},
    {"key": "Aug 2020", "values": [24.8, 17.2]},
    {"key": "Sep 2020", "values": [32.5, 23.9]},
    {"key": "Oct 2020", "values": [36.7, 27.1]},
    {"key": "Nov 2020", "values": [34.7, 28.1]},
    {"key": "Dec 2020", "values": [42.7, 33.1]},
    {"key": "Jan 2021", "values": [39.7, 36.1]},
]
_DEFAULT_COLORS: list[str] = ["#B89DFB", "#e7deff"]

client_tooltip_asset()
_PATH = rx.asset("bar_chart_multi_vertical.tsx", shared=True)


class BarChartMultiVertical(rx.NoSSRComponent):
    """Reflex wrapper around the parametrized BarChartMultiVertical TSX."""

    library = f"$/public{_PATH}"
    tag = "BarChartMultiVertical"
    is_default = False

    lib_dependencies: list[str] = ["d3"]

    data: rx.Var[list[MultiBarItem]] = rx.Var.create(_DEFAULT_DATA)
    colors: rx.Var[list[str]] = rx.Var.create(_DEFAULT_COLORS)


def bar_chart_multi_vertical(**props) -> rx.Component:
    """Grouped vertical bar chart with a per-group tooltip.

    Args:
        data: list of ``{"key": str, "values": list[float]}``. Defaults to the original
            rosencharts example.
        colors: palette (CSS colors) for the bars within each group. Defaults to
            ``["#B89DFB", "#e7deff"]``.

    Returns:
        A Reflex component rendering the grouped vertical bar chart.
    """
    return BarChartMultiVertical.create(**props)
