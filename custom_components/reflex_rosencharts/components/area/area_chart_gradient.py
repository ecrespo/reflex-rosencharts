"""Gradient area chart wrapper (port of rosencharts ``area-charts/3_AreaChartGradient``).

Data schema: ``list[{"date": str (YYYY-MM-DD), "value": float}]``. Empty data
renders an empty container (never raises). With no ``data`` the original
rosencharts example dataset is shown.
"""

import reflex as rx

# Importing this registers the shared ClientTooltip.tsx asset (symlink) that the
# chart TSX imports via the $/public alias.
from ..helpers import client_tooltip as _client_tooltip  # noqa: F401

# Copy the local TSX into the generated frontend and expose it as a component.
_path = rx.asset("./area_chart_gradient.tsx", shared=True)


class AreaChartGradient(rx.NoSSRComponent):
    """D3 + Tailwind gradient-filled area chart. NoSSR because the tooltip uses a DOM portal."""

    library = f"$/public{_path}"
    tag = "AreaChartGradient"
    is_default = False

    # The TSX imports from "d3"; ensure it is installed in the frontend.
    lib_dependencies: list[str] = ["d3@^7.9.0"]

    # data: list[{"date": str, "value": float}]
    data: rx.Var[list[dict]]


def area_chart_gradient(**props) -> rx.Component:
    """Render a gradient area chart. Pass ``data=[{"date": ..., "value": ...}, ...]``."""
    return AreaChartGradient.create(**props)
