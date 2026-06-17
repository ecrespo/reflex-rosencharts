# Contributing — Port recipe (rosencharts → Reflex)

A repeatable pattern for porting each chart. Details in
[`specs/technical/architecture.md`](specs/technical/architecture.md) §5.2.

## Steps per chart

1. **Copy** `reference/rosencharts/<family>/<n>_<Name>.tsx`
   → `reflex_rosencharts/components/<family>/<name>.tsx`.
2. **Parametrize the data**: replace the hardcoded `data` with a prop whose default matches the
   original example:
   ```tsx
   const defaultData = [ ...ejemplo original... ];
   export function ChartName({ data = defaultData, color = "..." }: {...}) {
     if (data.length === 0) return <div className="relative h-72 w-full" />;
     // ... mapear/escalas a partir de `data`
   }
   ```
3. **Adjust the helper imports** to the local path (`./helpers/ClientTooltip` or relative).
4. **Python wrapper** (`<name>.py`):
   ```python
   from typing import TypedDict
   import reflex as rx
   from ..helpers.client_tooltip import client_tooltip_asset  # sólo si usa tooltip

   class LinePoint(TypedDict):
       date: str
       value: float

   _DEFAULT_DATA: list[LinePoint] = [ ...ejemplo... ]

   client_tooltip_asset()                       # sólo si usa tooltip (lo hace viajar)
   _PATH = rx.asset("line_chart.tsx", shared=True)

   class LineChart(rx.Component):          # NoSSRComponent if it uses portal/tooltip
       library = f"$/public{_path}"
       tag = "LineChart"
       is_default = False
       lib_dependencies: list[str] = ["d3"]      # si el TSX importa de "d3"
       data: rx.Var[list[LinePoint]] = rx.Var.create(_DEFAULT_DATA)
       color: rx.Var[str] = rx.Var.create("stroke-fuchsia-400")

   def line_chart(**props) -> rx.Component:
       return LineChart.create(**props)
   ```
5. **Re-export** in `components/<family>/__init__.py` and in `reflex_rosencharts/__init__.py`.
6. **Example** in the gallery (`reflex_rosencharts/reflex_rosencharts.py`).
7. **Tests**: import + render; **visual comparison** via screenshot against `reference/`.

## Rules

- Python name in `snake_case`; drop the `_DIV` suffix (a render technique, document it in the docstring).
- Empty `data` ⇒ empty render, never raise an exception.
- Preserve Tailwind `dark:` variants.
- Each variant with extra fields defines its own `TypedDict` (see Data Model §4).

## Definition of Done (per chart)

- [ ] Wrapper + parametrized TSX + re-export
- [ ] Example in the gallery
- [ ] Tests green and compiles in the Reflex build
- [ ] Visual parity reviewed
- [ ] Docstring with data schema and snippet
