# Contribuir — Receta de port (rosencharts → Reflex)

Patrón repetible para portar cada gráfica. Detalle en
[`specs/technical/architecture.md`](specs/technical/architecture.md) §5.2.

## Pasos por gráfica

1. **Copiar** `reference/rosencharts/<familia>/<n>_<Name>.tsx`
   → `reflex_rosencharts/components/<familia>/<name>.tsx`.
2. **Parametrizar datos**: sustituir el `data` hardcodeado por una prop con default igual al
   ejemplo original:
   ```tsx
   export function LineChart({ data = DEFAULT_DATA, color = "stroke-fuchsia-400" }) { ... }
   ```
3. **Ajustar imports** del helper a la ruta local (`./helpers/ClientTooltip` o relativa).
4. **Wrapper Python** (`<name>.py`):
   ```python
   import reflex as rx
   from typing import TypedDict

   class LinePoint(TypedDict):
       date: str
       value: float

   _path = rx.asset("./line_chart.tsx", shared=True)

   class LineChart(rx.Component):          # NoSSRComponent si usa portal/tooltip
       library = f"$/public{_path}"
       tag = "LineChart"
       is_default = False
       data: rx.Var[list[LinePoint]] = rx.Var.create([])
       color: rx.Var[str] = rx.Var.create("stroke-fuchsia-400")
       on_point_hover: rx.EventHandler[rx.event.passthrough_event_spec(dict)]

   def line_chart(**props) -> rx.Component:
       return LineChart.create(**props)
   ```
5. **Re-exportar** en `components/<familia>/__init__.py` y en `reflex_rosencharts/__init__.py`.
6. **Ejemplo** en la galería (`reflex_rosencharts/reflex_rosencharts.py`).
7. **Tests**: import + render; **comparación visual** por captura contra `reference/`.

## Reglas

- Nombre Python en `snake_case`; quitar sufijo `_DIV` (técnica de render, va en el docstring).
- `data` vacío ⇒ render vacío, nunca lanzar excepción.
- Conservar variantes `dark:` de Tailwind.
- Cada variante con campos extra define su propio `TypedDict` (ver Data Model §4).

## Definición de Done (por gráfica)

- [ ] Wrapper + TSX parametrizado + re-export
- [ ] Ejemplo en galería
- [ ] Tests verdes y compila en build de Reflex
- [ ] Paridad visual revisada
- [ ] Docstring con esquema de datos y snippet
