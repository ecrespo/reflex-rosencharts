"""Horizontal bar chart with country flags (port of rosencharts
``bar-charts/7_BarChartFlagsHorizontal``).

Each row is preceded by a circular country flag (loaded from the public
circle-flags CDN by ISO code). Data schema:
``list[{"key": str, "value": float, "flag": str}]`` where ``flag`` is a
lowercase ISO 3166-1 alpha-2 code (e.g. ``"pt"``). Empty data renders an empty
container.
"""

import reflex as rx

_path = rx.asset("./bar_chart_flags_horizontal.tsx", shared=True)


class BarChartFlagsHorizontal(rx.NoSSRComponent):
    """D3 + Tailwind horizontal bar chart with flags."""

    library = f"$/public{_path}"
    tag = "BarChartFlagsHorizontal"
    is_default = False

    lib_dependencies: list[str] = ["d3@^7.9.0"]

    # data: list[{"key": str, "value": float, "flag": str}]
    data: rx.Var[list[dict]]


def bar_chart_flags_horizontal(**props) -> rx.Component:
    """Render a horizontal bar chart with flags. Pass ``data=[{"key", "value", "flag"}, ...]``."""
    return BarChartFlagsHorizontal.create(**props)
