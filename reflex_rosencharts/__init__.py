"""reflex-rosencharts: port de rosencharts a componentes de Reflex.

API pública (a poblar durante la implementación, ver specs/api/component-api-v1.md):
    import reflex_rosencharts as rxc
    rxc.line_chart(data=...)

Por ahora el paquete expone el scaffold y la demo app. Las funciones de gráfica
se irán re-exportando aquí a medida que se porten (fases F1-F7 del plan).
"""

__version__ = "0.0.1"

# Public API — aggregated dynamically from each family package so that charts can be
# ported in parallel without ever editing this shared file. Each family's __init__
# declares __all__; we lift those names into the package namespace.
import importlib as _importlib  # noqa: E402

_FAMILIES = ["line", "area", "bar", "pie", "scatter", "treemap", "radar", "other"]
__all__: list[str] = []

for _family in _FAMILIES:
    try:
        _mod = _importlib.import_module(f".components.{_family}", __name__)
    except ModuleNotFoundError:
        continue
    for _name in getattr(_mod, "__all__", []):
        globals()[_name] = getattr(_mod, _name)
        __all__.append(_name)

del _importlib, _family, _FAMILIES
