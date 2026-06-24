"""Treemap chart with images wrapper (port of rosencharts ``treemap-charts/2_TreemapChartImages_DIV``).

The ``_DIV`` suffix in the original refers to the render technique (each leaf is
an absolutely-positioned ``<div>`` placed with percentage coordinates from the
d3 treemap layout, not SVG rects); it is dropped from the public name. Each leaf
renders a logo ``<img>`` instead of text.

Data schema (nested hierarchy fed to ``d3.hierarchy``)::

    {
        "name": "root",
        "children": [
            {
                "name": "Tech",
                "children": [
                    {"name": "Apple", "value": 100, "logo": "https://.../apple.svg"},
                    ...
                ],
            },
            ...
        ],
    }

Top-level ``children`` are the topics (used for the ordinal color scale); their
``children`` are the leaves with a numeric ``value`` and an image ``logo`` URL.
Empty/missing data renders an empty container.
"""

import reflex as rx

from ..helpers import client_tooltip as _client_tooltip  # noqa: F401

_path = rx.asset("./treemap_chart_images.tsx", shared=True)


class TreemapChartImages(rx.NoSSRComponent):
    """D3 + Tailwind treemap chart with per-leaf logos. NoSSR (tooltip uses a DOM portal)."""

    library = f"$/public{_path}"
    tag = "TreemapChartImages"
    is_default = False

    lib_dependencies: list[str] = ["d3@^7.9.0"]

    # data: nested hierarchy {"name": str, "children": [{"name": str, "children": [{"name": str, "value": float, "logo": str}]}]}
    data: rx.Var[dict]


def treemap_chart_images(**props) -> rx.Component:
    """Render a treemap chart with logos. Pass ``data={"name": "root", "children": [...]}``."""
    return TreemapChartImages.create(**props)
