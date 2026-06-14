"""reflex-rosencharts: port de rosencharts a componentes de Reflex.

API pública (a poblar durante la implementación, ver specs/api/component-api-v1.md):
    import reflex_rosencharts as rxc
    rxc.line_chart(data=...)

Por ahora el paquete expone el scaffold y la demo app. Las funciones de gráfica
se irán re-exportando aquí a medida que se porten (fases F1-F7 del plan).
"""

__version__ = "0.0.1"

# Public API — re-exported per chart as families are ported.
from .components.line import line_chart  # noqa: E402

__all__ = ["line_chart"]
