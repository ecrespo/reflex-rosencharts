"""Treemap chart with gradients wrapper (port of rosencharts ``treemap-charts/3_TreemapChartGradient_DIV``).

The ``_DIV`` suffix in the original refers to the render technique (each leaf is
an absolutely-positioned ``<div>`` placed with percentage coordinates from the
d3 treemap layout, not SVG rects); it is dropped from the public name. Topics are
colored with vertical Tailwind gradients instead of flat fills.

Data schema (nested hierarchy fed to ``d3.hierarchy``)::

    {
        "name": "root",
        "children": [
            {
                "name": "Tech",
                "children": [
                    {"name": "Apple", "value": 100},
                    ...
                ],
            },
            ...
        ],
    }

Top-level ``children`` are the topics (used for the ordinal gradient scale);
their ``children`` are the leaves with a numeric ``value``. Empty/missing data
renders an empty container.
"""

import reflex as rx

from ..helpers import client_tooltip as _client_tooltip  # noqa: F401

_path = rx.asset("./treemap_chart_gradient.tsx", shared=True)


class TreemapChartGradient(rx.NoSSRComponent):
    """D3 + Tailwind treemap chart with gradient topics. NoSSR (tooltip uses a DOM portal)."""

    library = f"$/public{_path}"
    tag = "TreemapChartGradient"
    is_default = False

    lib_dependencies: list[str] = ["d3@^7.9.0"]

    # data: nested hierarchy {"name": str, "children": [{"name": str, "children": [{"name": str, "value": float}]}]}
    data: rx.Var[dict]


def treemap_chart_gradient(**props) -> rx.Component:
    """Render a gradient treemap chart. Pass ``data={"name": "root", "children": [...]}``."""
    return TreemapChartGradient.create(**props)
