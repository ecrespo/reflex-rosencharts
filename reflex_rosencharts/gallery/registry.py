"""Gallery registry: collects one example entry per ported chart.

Each chart family declares its own ``GALLERY_ENTRIES`` list in
``reflex_rosencharts/components/<family>/gallery.py``. This central registry imports
them defensively so that families ported in parallel never conflict on a shared file,
and a not-yet-ported family simply contributes nothing.
"""

from __future__ import annotations

import importlib
from dataclasses import dataclass
from typing import Callable

import reflex as rx


@dataclass(frozen=True)
class ChartEntry:
    """One gallery card: a chart rendered with its default example + usage snippet."""

    name: str  # public function name, e.g. "line_chart"
    title: str  # human label, e.g. "Line Chart"
    family: str  # family key, e.g. "line"
    render: Callable[[], rx.Component]  # zero-arg render of the example
    snippet: str  # Python usage snippet shown next to the chart


# Display order of families in the sidebar.
FAMILIES: list[tuple[str, str]] = [
    ("line", "Line"),
    ("area", "Area"),
    ("bar", "Bar"),
    ("pie", "Pie / Donut"),
    ("scatter", "Scatter"),
    ("treemap", "Treemap"),
    ("radar", "Radar"),
    ("other", "Other"),
]


def _load_family_entries(family: str) -> list[ChartEntry]:
    """Import ``components.<family>.gallery`` and return its GALLERY_ENTRIES (or [])."""
    try:
        mod = importlib.import_module(
            f"reflex_rosencharts.components.{family}.gallery"
        )
    except ModuleNotFoundError:
        return []
    return list(getattr(mod, "GALLERY_ENTRIES", []))


def all_entries() -> dict[str, list[ChartEntry]]:
    """Return ``{family_key: [ChartEntry, ...]}`` for every family with ported charts."""
    return {key: _load_family_entries(key) for key, _ in FAMILIES}
