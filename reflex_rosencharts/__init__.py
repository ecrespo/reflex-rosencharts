"""reflex-rosencharts: a port of rosencharts to Reflex components.

Public API (to be populated during implementation, see specs/api/component-api-v1.md):
    import reflex_rosencharts as rxc
    rxc.line_chart(data=...)

For now the package exposes the scaffold and the demo app. The chart functions
will be re-exported here as they are ported (phases F1-F7 of the plan).
"""

__version__ = "0.1.1"

# Re-export example (enabled as each chart is ported):
# from .components.line.line_chart import line_chart  # noqa: F401
