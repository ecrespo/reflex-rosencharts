"""Base component wrapper for the reflex-rosencharts charts.

The individual chart functions (``line_chart``, ``bar_chart``, ...) are implemented
under ``reflex_rosencharts.components.<family>`` and re-exported from the package
``__init__``. This module holds the shared base class they build on.

See ``specs/`` for the full SDD plan and the public Python API contract
(``specs/api/component-api-v1.md``). Charts are ported incrementally in phases
F1-F7; only ported charts are exported.
"""

import reflex as rx


class RosenChart(rx.Component):
    """Base class for all rosencharts chart wrappers.

    Each ported chart subclasses this and sets ``tag``/``library`` (or supplies
    inline TSX via ``_get_custom_code``). The base class is intentionally not a
    usable chart on its own; it exists so the package imports cleanly and the
    Reflex build tooling has a stable entry point while charts are being ported.
    """

    # The React library to wrap. Concrete charts set this as they are ported.
    library = ""

    # The React component tag. Concrete charts set this as they are ported.
    tag = ""


# Bound factory (no chart is instantiated until a concrete subclass sets tag/library).
rosen_chart = RosenChart.create