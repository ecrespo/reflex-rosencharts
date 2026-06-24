"""Treemap chart wrapper (port of rosencharts ``treemap-charts/1_TreemapChart_DIV``).

The ``_DIV`` suffix in the original refers to the render technique (each leaf is
an absolutely-positioned ``<div>`` placed with percentage coordinates from the
d3 treemap layout, not SVG rects); it is dropped from the public name.

Data schema (nested hierarchy fed to ``d3.hierarchy``)::

    {
        "name": "root",
        "children": [
            {
                "name": "Tech",
                "children": [
                    {"name": "Windows", "value": 100},
                    {"name": "MacOS", "value": 120},
                ],
            },
            ...
        ],
    }

Top-level ``children`` are the topics (used for the ordinal color scale); their
``children`` are the leaves with a numeric ``value``. Empty/missing data renders
an empty container.
"""

import reflex as rx

from ..helpers import client_tooltip as _client_tooltip  # noqa: F401

_path = rx.asset("./treemap_chart.tsx", shared=True)


class TreemapChart(rx.NoSSRComponent):
    """D3 + Tailwind treemap chart. NoSSR (tooltip uses a DOM portal)."""

    library = f"$/public{_path}"
    tag = "TreemapChart"
    is_default = False

    lib_dependencies: list[str] = ["d3@^7.9.0"]

    # data: nested hierarchy {"name": str, "children": [{"name": str, "children": [{"name": str, "value": float}]}]}
    data: rx.Var[dict]


def treemap_chart(**props) -> rx.Component:
    """Render a treemap chart. Pass ``data={"name": "root", "children": [...]}``."""
    return TreemapChart.create(**props)
