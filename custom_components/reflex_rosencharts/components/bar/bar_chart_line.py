"""Combined bar + line chart (port of rosencharts ``bar-charts/14_BarChartLine``).

Dual-axis chart: ``metric1`` is drawn as gradient bars against the left axis and
``metric2`` as a smooth (monotone) line against the right axis. Pads the dataset
with empty bars up to a minimum count; x-axis labels are rotated 45deg. Data
schema: ``list[{"key": str, "metric1": float, "metric2": float}]``. Empty data
renders an empty container.
"""

import reflex as rx

from ..helpers import client_tooltip as _client_tooltip  # noqa: F401

_path = rx.asset("./bar_chart_line.tsx", shared=True)


class BarChartLine(rx.NoSSRComponent):
    """D3 + Tailwind combined bar + line chart. NoSSR (tooltip uses a DOM portal)."""

    library = f"$/public{_path}"
    tag = "BarChartLine"
    is_default = False

    lib_dependencies: list[str] = ["d3@^7.9.0"]

    # data: list[{"key": str, "metric1": float, "metric2": float}]
    data: rx.Var[list[dict]]


def bar_chart_line(**props) -> rx.Component:
    """Render a combined bar + line chart. Pass ``data=[{"key", "metric1", "metric2"}, ...]``."""
    return BarChartLine.create(**props)
