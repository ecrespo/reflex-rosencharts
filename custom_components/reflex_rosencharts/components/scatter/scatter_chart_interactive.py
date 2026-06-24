"""Interactive scatter chart wrapper (port of rosencharts
``scatter-charts/2_ScatterChartInteractive``).

Data schema: ``list[{"revenue": float, "value": float, "company": str}]``.
``revenue`` is the x value, ``value`` is the y value, ``company`` labels the
tooltip. Clicking a point fires ``on_point_click`` with the point dict. Empty
data renders an empty container of the same size. With no ``data`` the original
rosencharts example dataset is shown.
"""

import reflex as rx

from ..helpers import client_tooltip as _client_tooltip  # noqa: F401

_path = rx.asset("./scatter_chart_interactive.tsx", shared=True)


class ScatterChartInteractive(rx.NoSSRComponent):
    """D3 + Tailwind interactive scatter chart. NoSSR because the tooltip uses a DOM portal."""

    library = f"$/public{_path}"
    tag = "ScatterChartInteractive"
    is_default = False

    lib_dependencies: list[str] = ["d3@^7.9.0"]

    # data: list[{"revenue": float, "value": float, "company": str}]
    data: rx.Var[list[dict]]

    # Fired with the clicked point dict {"revenue", "value", "company"}.
    on_point_click: rx.EventHandler[rx.event.passthrough_event_spec(dict)]


def scatter_chart_interactive(**props) -> rx.Component:
    """Render an interactive scatter chart.

    Pass ``data=[{"revenue": ..., "value": ..., "company": ...}, ...]`` and an
    optional ``on_point_click`` handler that receives the clicked point dict.
    """
    return ScatterChartInteractive.create(**props)
