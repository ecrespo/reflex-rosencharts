"""bar_chart_breakdown — port of rosencharts bar-charts/4_BarChartBreakdown.tsx.

Render technique: DIV-based stacked horizontal segments (a single 54px-tall bar split
into width-proportional gradient segments, each labelled with its key and value). No
D3, no tooltip, so this subclasses ``rx.Component`` (not NoSSR).

Data schema (``BreakdownItem``)::

    {"key": str, "value": float, "color": str}  # color = Tailwind from-*/to-* classes

Example::

    import reflex_rosencharts as rxc
    rxc.bar_chart_breakdown(data=State.allocation)
"""

from typing import TypedDict

import reflex as rx


class BreakdownItem(TypedDict):
    """A breakdown segment with a Tailwind gradient color spec."""

    key: str
    value: float
    color: str  # Tailwind 'from-* to-*' classes


_DEFAULT_DATA: list[BreakdownItem] = [
    {
        "key": "Utils",
        "value": 17.1,
        "color": "from-fuchsia-300/80 to-fuchsia-400/80 dark:from-fuchsia-500 dark:to-fuchsia-700",
    },
    {
        "key": "Tech",
        "value": 14.3,
        "color": "from-violet-300 to-violet-400 dark:from-violet-500 dark:to-violet-700",
    },
    {
        "key": "Energy",
        "value": 27.1,
        "color": "from-blue-300 to-blue-400 dark:from-blue-500 dark:to-blue-700",
    },
    {
        "key": "Cyclicals",
        "value": 42.5,
        "color": "from-sky-300 to-sky-400 dark:from-sky-500 dark:to-sky-700",
    },
    {
        "key": "Fuel",
        "value": 12.7,
        "color": "from-orange-200 to-orange-300 dark:from-amber-500 dark:to-amber-700",
    },
]

_PATH = rx.asset("bar_chart_breakdown.tsx", shared=True)


class BarChartBreakdown(rx.Component):
    """Reflex wrapper around the parametrized BarChartBreakdown TSX."""

    library = f"$/public{_PATH}"
    tag = "BarChartBreakdown"
    is_default = False

    data: rx.Var[list[BreakdownItem]] = rx.Var.create(_DEFAULT_DATA)


def bar_chart_breakdown(**props) -> rx.Component:
    """Single horizontal bar split into proportional, labelled gradient segments.

    Args:
        data: list of ``{"key": str, "value": float, "color": str}``. Defaults to the
            original rosencharts example.

    Returns:
        A Reflex component rendering the breakdown bar.
    """
    return BarChartBreakdown.create(**props)
