"""radar_chart_rounded — port of rosencharts radar-charts/8_RadarChartRounded.tsx.

Render technique: SVG radar (spider) chart computed with D3 (scaleLinear +
d3.lineRadial with curveCardinalClosed for a rounded outline), with banded
concentric rings and per-point value bubbles, styled with Tailwind. No tooltip,
so the component is a plain ``rx.Component``.

Data schema (``RadarPoint``)::

    {"topic": str, "value": float}

Example::

    import reflex_rosencharts as rxc
    rxc.radar_chart_rounded(data=State.metrics)
"""

from typing import TypedDict

import reflex as rx


class RadarPoint(TypedDict):
    """A single axis of a radar chart."""

    topic: str
    value: float


# Default dataset == the original rosencharts example, so ``radar_chart_rounded()``
# with no args reproduces the reference chart (Tech Design DD-002).
_DEFAULT_DATA: list[RadarPoint] = [
    {"topic": "Tech", "value": 320},
    {"topic": "Financials", "value": 190},
    {"topic": "Energy", "value": 170},
    {"topic": "Healthcare", "value": 250},
    {"topic": "Utilities", "value": 210},
]

_PATH = rx.asset("radar_chart_rounded.tsx", shared=True)


class RadarChartRounded(rx.Component):
    """Reflex wrapper around the parametrized RadarChartRounded TSX."""

    library = f"$/public{_PATH}"
    tag = "RadarChartRounded"
    is_default = False

    lib_dependencies: list[str] = ["d3"]

    # Props
    data: rx.Var[list[RadarPoint]] = rx.Var.create(_DEFAULT_DATA)


def radar_chart_rounded(**props) -> rx.Component:
    """Rounded radar (spider) chart with banded rings and value bubbles.

    Args:
        data: list of ``{"topic": str, "value": float}``. Defaults to the
            original rosencharts example.

    Returns:
        A Reflex component rendering the rounded radar chart.
    """
    return RadarChartRounded.create(**props)
