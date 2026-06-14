# Contribuir — Receta de port (rosencharts → Reflex)

Patrón **probado** (validado end-to-end con el piloto `line_chart`, compila con
`reflex export`). Detalle de diseño en
[`specs/technical/architecture.md`](specs/technical/architecture.md) §5.2.

## Layout de assets (importante)

`rx.asset("x.tsx", shared=True)` copia el archivo a
`public/external/<módulo_python_punteado_como_dirs>/x.tsx`. Es decir, el módulo
`reflex_rosencharts.components.line.line_chart` deja su TSX en
`external/reflex_rosencharts/components/line/line_chart/line_chart.tsx`.

Como **toda** gráfica vive en `components/<familia>/<name>.py` (asset = `<name>.tsx`),
su TSX queda en `.../components/<familia>/<name>/<name>.tsx`, y el helper compartido
en `.../components/helpers/client_tooltip/ClientTooltip.tsx`. Por eso la ruta relativa
al helper es **constante para todas las gráficas**:

```tsx
import { ClientTooltip, TooltipTrigger, TooltipContent } from "../../helpers/client_tooltip/ClientTooltip";
```

## Pasos por gráfica (TDD)

1. **RED** — `tests/test_<familia>.py`: la función existe, es importable, `.create(data=...)`
   construye un `rx.Component`, y el default reproduce el ejemplo. Corre el test y velo fallar.
2. **Copiar** `reference/rosencharts/<familia>-charts/<n>_<Name>.tsx`
   → `reflex_rosencharts/components/<familia>/<name>.tsx`.
3. **Parametrizar datos**: sustituir el array hardcodeado por una prop con default = ejemplo:
   ```tsx
   const defaultData = [ ...ejemplo original... ];
   export function ChartName({ data = defaultData, color = "..." }: {...}) {
     if (data.length === 0) return <div className="relative h-72 w-full" />;
     // ... mapear/escalas a partir de `data`
   }
   ```
4. **Ajustar import del helper** (sólo si usa tooltip) a la ruta constante de arriba.
5. **Wrapper Python** (`<name>.py`):
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

   class LineChart(rx.NoSSRComponent):          # NoSSRComponent si usa portal/tooltip; rx.Component si no
       library = f"$/public{_PATH}"
       tag = "LineChart"                         # == nombre exportado en el TSX
       is_default = False
       lib_dependencies: list[str] = ["d3"]      # si el TSX importa de "d3"
       data: rx.Var[list[LinePoint]] = rx.Var.create(_DEFAULT_DATA)
       color: rx.Var[str] = rx.Var.create("stroke-fuchsia-400")

   def line_chart(**props) -> rx.Component:
       return LineChart.create(**props)
   ```
6. **Re-exportar** en `components/<familia>/__init__.py` y en `reflex_rosencharts/__init__.py`.
7. **Entrada de galería** en `components/<familia>/gallery.py` (lista `GALLERY_ENTRIES`); el
   registry central la recoge sin tocar archivos compartidos.
8. **GREEN** — corre el test y velo pasar. Refactor manteniendo verde. Commit.

## Reglas

- Nombre Python en `snake_case`; quitar sufijo `_DIV` (técnica de render, va en el docstring).
- `tag` debe coincidir EXACTAMENTE con el nombre `export function <Tag>` del TSX.
- `data` vacío ⇒ render de contenedor vacío, nunca lanzar excepción.
- Conservar variantes `dark:` de Tailwind.
- Cada variante con campos extra define su propio `TypedDict` (ver Data Model §4).
- Gráficas SIN tooltip: usar `rx.Component` (no NoSSR) y omitir `client_tooltip_asset()`.

## Definición de Done (por gráfica)

- [ ] Test TDD verde (import + render + default)
- [ ] Wrapper + TSX parametrizado + re-export en ambos `__init__`
- [ ] Entrada en `components/<familia>/gallery.py`
- [ ] Compila en `reflex export`
- [ ] Docstring con esquema de datos y snippet
