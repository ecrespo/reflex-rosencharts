"""bar_chart_horizontal_logo — port of bar-charts/2_BarChartHorizontalLogo_DIV.tsx.

Render technique: DIV-based bars with D3 scales. Per-bar company logos are built-in
inline SVGs picked by index (the original hardcodes 6 logos), so they are not
data-driven; the ``data`` only controls keys, values and bar colors. Uses the shared
ClientTooltip helper, so the component is client-side only (NoSSRComponent). The
``_DIV`` suffix is dropped (render technique only).

Data schema (``LogoBarItem``)::

    {"key": str, "value": float, "color": str}  # color = Tailwind bg-* classes

Example::

    import reflex_rosencharts as rxc
    rxc.bar_chart_horizontal_logo(data=State.companies)
"""

from typing import TypedDict

import reflex as rx

from ..helpers.client_tooltip import client_tooltip_asset


class LogoBarItem(TypedDict):
    """A bar with a Tailwind background-color class."""

    key: str
    value: float
    color: str  # Tailwind 'bg-*' classes


_DEFAULT_DATA: list[LogoBarItem] = [
    {"key": "Company A", "value": 55.8, "color": "bg-pink-300 dark:bg-pink-400"},
    {"key": "Company B", "value": 34.3, "color": "bg-purple-300 dark:bg-purple-400"},
    {"key": "Company C", "value": 27.1, "color": "bg-indigo-300 dark:bg-indigo-400"},
    {"key": "Company D", "value": 22.5, "color": "bg-sky-300 dark:bg-sky-400"},
    {"key": "Company E", "value": 18.7, "color": "bg-orange-300 dark:bg-orange-400"},
    {"key": "Spanish or vanish", "value": 10.8, "color": "bg-lime-400 dark:bg-lime-500"},
]

client_tooltip_asset()
_PATH = rx.asset("bar_chart_horizontal_logo.tsx", shared=True)


class BarChartHorizontalLogo(rx.NoSSRComponent):
    """Reflex wrapper around the parametrized BarChartHorizontalLogo TSX."""

    library = f"$/public{_PATH}"
    tag = "BarChartHorizontalLogo"
    is_default = False

    lib_dependencies: list[str] = ["d3"]

    data: rx.Var[list[LogoBarItem]] = rx.Var.create(_DEFAULT_DATA)


def bar_chart_horizontal_logo(**props) -> rx.Component:
    """Horizontal bar chart with per-bar logos (index-based) and tooltip.

    Args:
        data: list of ``{"key": str, "value": float, "color": str}``. Defaults to the
            original rosencharts example. Logos are built-in inline SVGs chosen by row
            index, not by data.

    Returns:
        A Reflex component rendering the logo horizontal bar chart.
    """
    return BarChartHorizontalLogo.create(**props)
