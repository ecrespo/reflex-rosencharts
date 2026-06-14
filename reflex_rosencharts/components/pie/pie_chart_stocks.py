"""pie_chart_stocks — port of rosencharts pie-charts/2_PieChartStocks.tsx to Reflex.

Render technique: D3 ``pie``/``arc`` slices coloured per-item via Tailwind classes,
with connecting lines and logo/value labels positioned as absolute divs. Uses the
shared ClientTooltip helper (createPortal), so the component is client-side only
(NoSSRComponent).

Data schema (``StockSlice``)::

    {"name": str, "value": float, "logo": str, "color": str}

``color`` is a Tailwind ``text-*`` class applied to the slice & connector line.

Example::

    import reflex_rosencharts as rxc
    rxc.pie_chart_stocks(data=State.holdings)
"""

from typing import TypedDict

import reflex as rx

from ..helpers.client_tooltip import client_tooltip_asset


class StockSlice(TypedDict):
    """A pie slice with a logo and a Tailwind colour class."""

    name: str
    value: float
    logo: str  # image URL
    color: str  # Tailwind text-* class


_DEFAULT_DATA: list[StockSlice] = [
    {
        "name": "Apple",
        "value": 731,
        "logo": "https://etoro-cdn.etorostatic.com/market-avatars/1001/1001_494D5A_F7F7F7.svg",
        "color": "text-pink-400",
    },
    {
        "name": "Mercedes",
        "value": 631,
        "logo": "https://etoro-cdn.etorostatic.com/market-avatars/1206/1206_2F3350_F7F7F7.svg",
        "color": "text-purple-400",
    },
    {
        "name": "Palantir",
        "value": 331,
        "logo": "https://etoro-cdn.etorostatic.com/market-avatars/7991/7991_2C2C2C_F7F7F7.svg",
        "color": "text-indigo-400",
    },
    {
        "name": "Google",
        "value": 232,
        "logo": "https://etoro-cdn.etorostatic.com/market-avatars/1002/1002_3183FF_F7F7F7.svg",
        "color": "text-sky-400",
    },
    {
        "name": "Tesla",
        "value": 101,
        "logo": "https://etoro-cdn.etorostatic.com/market-avatars/1007/1007_F7F7F7_2C2C2C.svg",
        "color": "text-lime-400",
    },
    {
        "name": "Meta",
        "value": 42,
        "logo": "https://etoro-cdn.etorostatic.com/market-avatars/1008/1008_F7F7F7_2C2C2C.svg",
        "color": "text-amber-400",
    },
]

client_tooltip_asset()
_PATH = rx.asset("pie_chart_stocks.tsx", shared=True)


class PieChartStocks(rx.NoSSRComponent):
    """Reflex wrapper around the parametrized PieChartStocks TSX."""

    library = f"$/public{_PATH}"
    tag = "PieChartStocks"
    is_default = False

    lib_dependencies: list[str] = ["d3"]

    data: rx.Var[list[StockSlice]] = rx.Var.create(_DEFAULT_DATA)


def pie_chart_stocks(**props) -> rx.Component:
    """Pie chart with per-slice logos, connecting lines and a tooltip.

    Args:
        data: list of ``{"name", "value", "logo", "color"}`` where ``color`` is a
            Tailwind ``text-*`` class. Defaults to the original rosencharts example.

    Returns:
        A Reflex component rendering the stocks pie chart.
    """
    return PieChartStocks.create(**props)
