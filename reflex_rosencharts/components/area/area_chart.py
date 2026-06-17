"""area_chart — port of rosencharts area-charts/1_AreaChart.tsx to Reflex.

Render technique: D3 ``scaleTime``/``scaleLinear`` with ``d3.area`` + ``d3.line``
(curveMonotoneX), styled with Tailwind. Uses the shared ClientTooltip helper
(createPortal), so the component renders client-side only (NoSSRComponent).

Data schema (``AreaPoint``)::

    {"date": "YYYY-MM-DD", "value": float}

Example::

    import reflex_rosencharts as rxc
    rxc.area_chart(data=State.sales, color="text-purple-200 dark:text-purple-400")
"""

from typing import TypedDict

import reflex as rx

from ..helpers.client_tooltip import client_tooltip_asset


class AreaPoint(TypedDict):
    """A single point of a time series."""

    date: str  # ISO date 'YYYY-MM-DD'
    value: float


# Default dataset == the original rosencharts example, so ``area_chart()`` with no
# args reproduces the reference chart (Tech Design DD-002).
_DEFAULT_DATA: list[AreaPoint] = [
    {"date": "2023-04-30", "value": 4},
    {"date": "2023-05-01", "value": 6},
    {"date": "2023-05-02", "value": 8},
    {"date": "2023-05-03", "value": 7},
    {"date": "2023-05-04", "value": 10},
    {"date": "2023-05-05", "value": 12},
    {"date": "2023-05-06", "value": 10.5},
    {"date": "2023-05-07", "value": 6},
    {"date": "2023-05-08", "value": 8},
    {"date": "2023-05-09", "value": 7.5},
    {"date": "2023-05-10", "value": 6},
    {"date": "2023-05-11", "value": 8},
    {"date": "2023-05-12", "value": 9},
    {"date": "2023-05-13", "value": 10},
    {"date": "2023-05-14", "value": 17},
    {"date": "2023-05-15", "value": 14},
    {"date": "2023-05-16", "value": 15},
    {"date": "2023-05-17", "value": 20},
    {"date": "2023-05-18", "value": 18},
    {"date": "2023-05-19", "value": 16},
    {"date": "2023-05-20", "value": 15},
    {"date": "2023-05-21", "value": 16},
    {"date": "2023-05-22", "value": 13},
    {"date": "2023-05-23", "value": 11},
    {"date": "2023-05-24", "value": 11},
    {"date": "2023-05-25", "value": 13},
    {"date": "2023-05-26", "value": 12},
    {"date": "2023-05-27", "value": 9},
    {"date": "2023-05-28", "value": 8},
    {"date": "2023-05-29", "value": 10},
    {"date": "2023-05-30", "value": 11},
    {"date": "2023-05-31", "value": 8},
    {"date": "2023-06-01", "value": 9},
    {"date": "2023-06-02", "value": 10},
    {"date": "2023-06-03", "value": 12},
    {"date": "2023-06-04", "value": 13},
    {"date": "2023-06-05", "value": 15},
    {"date": "2023-06-06", "value": 13.5},
    {"date": "2023-06-07", "value": 13},
    {"date": "2023-06-08", "value": 13},
    {"date": "2023-06-09", "value": 14},
    {"date": "2023-06-10", "value": 13},
    {"date": "2023-06-11", "value": 12.5},
]

# Ship the shared helper next to this chart so the TSX's relative import resolves.
client_tooltip_asset()
_PATH = rx.asset("area_chart.tsx", shared=True)


class AreaChart(rx.NoSSRComponent):
    """Reflex wrapper around the parametrized AreaChart TSX."""

    library = f"$/public{_PATH}"
    tag = "AreaChart"
    is_default = False

    lib_dependencies: list[str] = ["d3"]

    # Props
    data: rx.Var[list[AreaPoint]] = rx.Var.create(_DEFAULT_DATA)
    color: rx.Var[str] = rx.Var.create("text-purple-200 dark:text-purple-400")


def area_chart(**props) -> rx.Component:
    """Filled area chart over a time series, with a per-point tooltip.

    Args:
        data: list of ``{"date": "YYYY-MM-DD", "value": float}``. Defaults to the
            original rosencharts example.
        color: Tailwind ``text-*`` class for the filled area. Defaults to
            ``"text-purple-200 dark:text-purple-400"``.

    Returns:
        A Reflex component rendering the area chart.
    """
    return AreaChart.create(**props)
