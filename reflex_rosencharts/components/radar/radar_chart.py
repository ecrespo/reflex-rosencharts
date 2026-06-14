"""radar_chart — port of rosencharts radar-charts/6_RadarChart.tsx to Reflex.

Render technique: SVG radar (spider) chart computed with D3 (scaleLinear +
d3.lineRadial with curveLinearClosed), styled with Tailwind. No tooltip, so the
component is a plain ``rx.Component``.

Data schema (``RadarPoint``)::

    {"topic": str, "value": float}

Example::

    import reflex_rosencharts as rxc
    rxc.radar_chart(data=State.metrics)
"""

from typing import TypedDict

import reflex as rx


class RadarPoint(TypedDict):
    """A single axis of a radar chart."""

    topic: str
    value: float


# Default dataset == the original rosencharts example, so ``radar_chart()`` with no
# args reproduces the reference chart (Tech Design DD-002).
_DEFAULT_DATA: list[RadarPoint] = [
    {"topic": "Tech", "value": 330},
    {"topic": "Financials", "value": 160},
    {"topic": "Energy", "value": 140},
    {"topic": "Healthcare", "value": 200},
    {"topic": "Utilities", "value": 180},
]

_PATH = rx.asset("radar_chart.tsx", shared=True)


class RadarChart(rx.Component):
    """Reflex wrapper around the parametrized RadarChart TSX."""

    library = f"$/public{_PATH}"
    tag = "RadarChart"
    is_default = False

    lib_dependencies: list[str] = ["d3"]

    # Props
    data: rx.Var[list[RadarPoint]] = rx.Var.create(_DEFAULT_DATA)


def radar_chart(**props) -> rx.Component:
    """Radar (spider) chart over a set of topic/value axes.

    Args:
        data: list of ``{"topic": str, "value": float}``. Defaults to the
            original rosencharts example.

    Returns:
        A Reflex component rendering the radar chart.
    """
    return RadarChart.create(**props)
