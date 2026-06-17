"""scatter_chart_multiclass — port of rosencharts scatter-charts/5_ScatterChartMulticlass.tsx.

Render technique: SVG points (D3 ``scaleLinear`` on both axes) in a 0-100 viewBox,
styled with Tailwind. Uses the shared ClientTooltip helper (createPortal) → rendered
client-side only (NoSSRComponent). The original two hardcoded series are merged into a
single ``data`` array; each point carries a ``class`` field used to pick its dot color
from ``class_colors``.

Data schema (``ScatterClassPoint``)::

    {"revenue": float (x), "value": float (y), "company": str, "class": str}

Example::

    import reflex_rosencharts as rxc
    rxc.scatter_chart_multiclass(
        data=State.points,
        class_colors={"green": "text-lime-500", "blue": "text-sky-500"},
    )
"""

from typing import TypedDict

import reflex as rx

from ..helpers.client_tooltip import client_tooltip_asset


class ScatterClassPoint(TypedDict):
    """A scatter point with a class label used for coloring."""

    revenue: float
    value: float
    company: str
    # `class` is a Python keyword, so it can't be a TypedDict attr name directly;
    # callers pass the dict literal with a "class" string key, which serializes fine.


# Default dataset == the original rosencharts example (two series, green + blue).
_DEFAULT_DATA: list[dict] = [
    {"revenue": 10, "value": 102.8, "company": "Green A", "class": "green"},
    {"revenue": 20, "value": 101.9, "company": "Green B", "class": "green"},
    {"revenue": 30, "value": 101.5, "company": "Green C", "class": "green"},
    {"revenue": 40, "value": 100.8, "company": "Green D", "class": "green"},
    {"revenue": 50, "value": 99.7, "company": "Green E", "class": "green"},
    {"revenue": 60, "value": 98.5, "company": "Green F", "class": "green"},
    {"revenue": 10, "value": 98.3, "company": "Blue A", "class": "blue"},
    {"revenue": 20, "value": 102.7, "company": "Blue B", "class": "blue"},
    {"revenue": 30, "value": 97.4, "company": "Blue C", "class": "blue"},
    {"revenue": 40, "value": 99.2, "company": "Blue D", "class": "blue"},
    {"revenue": 50, "value": 103.8, "company": "Blue E", "class": "blue"},
    {"revenue": 60, "value": 96.5, "company": "Blue F", "class": "blue"},
]

_DEFAULT_CLASS_COLORS: dict[str, str] = {
    "green": "text-lime-500",
    "blue": "text-sky-500",
}

client_tooltip_asset()
_PATH = rx.asset("scatter_chart_multiclass.tsx", shared=True)


class ScatterChartMulticlass(rx.NoSSRComponent):
    """Reflex wrapper around the parametrized ScatterChartMulticlass TSX."""

    library = f"$/public{_PATH}"
    tag = "ScatterChartMulticlass"
    is_default = False

    lib_dependencies: list[str] = ["d3"]

    data: rx.Var[list[dict]] = rx.Var.create(_DEFAULT_DATA)
    class_colors: rx.Var[dict[str, str]] = rx.Var.create(_DEFAULT_CLASS_COLORS)


def scatter_chart_multiclass(**props) -> rx.Component:
    """Scatter plot whose dot color is keyed by each point's ``class`` field.

    Args:
        data: list of ``{"revenue": x, "value": y, "company": label, "class": key}``.
            Defaults to the original rosencharts example (green + blue series).
        class_colors: mapping ``{class_key: tailwind text-* class}``. Defaults to
            ``{"green": "text-lime-500", "blue": "text-sky-500"}``.

    Returns:
        A Reflex component rendering the multiclass scatter chart.
    """
    return ScatterChartMulticlass.create(**props)
