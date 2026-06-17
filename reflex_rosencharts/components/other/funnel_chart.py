"""funnel_chart — port of rosencharts other-charts/5_FunnelChart.tsx to Reflex.

Render technique: centered, gradient-filled ``<div>`` bars stacked top-to-bottom,
each width proportional to its ``value`` (relative to the max), sorted by descending
value to form the funnel. No tooltip, no D3 — plain DIV layout, so the wrapper is a
plain ``rx.Component``.

The original embedded the gradient color in each datum; here data follows the spec
schema ``FunnelStage`` (``{name, value}``) and the per-stage gradient comes from the
``colors`` palette, indexed after sorting.

Data schema (``FunnelStage``)::

    {"name": str, "value": float}

Example::

    import reflex_rosencharts as rxc
    rxc.funnel_chart(data=State.pipeline)
"""

from typing import TypedDict

import reflex as rx


class FunnelStage(TypedDict):
    """One ordered stage of a funnel."""

    name: str
    value: float


# Default dataset == the original rosencharts example, so ``funnel_chart()`` with no
# args reproduces the reference chart (Tech Design DD-002).
_DEFAULT_DATA: list[FunnelStage] = [
    {"name": "Gross Revenue", "value": 47.1},
    {"name": "Net Revenue", "value": 32.3},
    {"name": "EBITDA", "value": 27.1},
    {"name": "Gross Profit", "value": 17.5},
    {"name": "Net Profit", "value": 12.7},
]

# Per-stage gradient classes (Tailwind ``bg-gradient-to-b`` stops), indexed by the
# sorted stage position. Matches the original example's palette.
_DEFAULT_COLORS: list[str] = [
    "from-pink-300 to-pink-400 dark:from-pink-500 dark:to-pink-700",
    "from-purple-400 to-purple-500 dark:from-purple-500 dark:to-purple-700",
    "from-indigo-400 to-indigo-500 dark:from-indigo-500 dark:to-indigo-700",
    "from-sky-400 to-sky-500 dark:from-sky-500 dark:to-sky-700",
    "from-orange-300 to-orange-400 dark:from-amber-500 dark:to-amber-700",
]

_PATH = rx.asset("funnel_chart.tsx", shared=True)


class FunnelChart(rx.Component):
    """Reflex wrapper around the parametrized FunnelChart TSX."""

    library = f"$/public{_PATH}"
    tag = "FunnelChart"
    is_default = False

    # Props
    data: rx.Var[list[FunnelStage]] = rx.Var.create(_DEFAULT_DATA)
    colors: rx.Var[list[str]] = rx.Var.create(_DEFAULT_COLORS)


def funnel_chart(**props) -> rx.Component:
    """Funnel chart of ordered stages, sorted by descending value.

    Args:
        data: list of ``{"name": str, "value": float}`` stages. Sorted descending by
            ``value`` for rendering; defaults to the original rosencharts example.
        colors: Tailwind gradient classes (``from-* to-* dark:...``) applied per
            stage by index. Defaults to the original 5-color palette.

    Returns:
        A Reflex component rendering the funnel chart.
    """
    return FunnelChart.create(**props)
