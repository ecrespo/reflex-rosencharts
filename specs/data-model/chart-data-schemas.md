# reflex-rosencharts — Data Model (esquemas de datos de las gráficas)

## Metadata

| Campo | Valor |
|---|---|
| **Autor** | Ernesto Crespo |
| **Estado** | `DRAFT` |
| **Versión** | 1.0 |
| **Fecha** | 2026-06-14 |
| **Tech Design** | [../technical/architecture.md](../technical/architecture.md) |
| **API Spec** | [../api/component-api-v1.md](../api/component-api-v1.md) |

---

> **Nota de adaptación SDD:** No hay base de datos. El "modelo de datos" de esta librería son los
> **esquemas de entrada** de cada gráfica: la forma del `data` que el desarrollador pasa desde
> `rx.State`. Se definen como `TypedDict` (interop directo con la estructura JS que espera el TSX).
> Donde Reflex deba convertir a camelCase, se usará `rx.PropsBase`.

## 1. Principios

- **Fidelidad con el original:** los nombres de campo replican los del TSX de rosencharts (p. ej.
  bar usa `key`, pie/donut usan `name`, scatter usa `revenue`/`value`/`company`).
- **Fechas como string ISO:** las series temporales reciben `date: "YYYY-MM-DD"`; el TSX las convierte
  con `new Date(...)` (como hace el original), evitando problemas de serialización Python↔JS.
- **Números como `float`/`int`:** sin `Decimal` (no es dato financiero transaccional, sólo visual).
- **Defaults = dataset del ejemplo original** (ver Tech Design DD-002).

## 2. Esquemas base

```python
from typing import TypedDict

# Serie temporal (line, area)
class TimePoint(TypedDict):
    date: str      # 'YYYY-MM-DD'
    value: float

# Categoría/valor (pie, donut)
class CategoryValue(TypedDict):
    name: str
    value: float

# Barra (bar charts) — el original usa la clave `key`
class BarItem(TypedDict):
    key: str
    value: float

# Punto de dispersión (scatter) — nombres del original
class ScatterPoint(TypedDict):
    revenue: float     # eje X
    value: float       # eje Y
    company: str       # etiqueta

# Radar
class RadarPoint(TypedDict):
    topic: str
    value: float

# Embudo (funnel)
class FunnelStage(TypedDict):
    name: str
    value: float

# Treemap (estructura anidada del original)
class TreemapNode(TypedDict):
    topic: str
    subtopics: list[dict]   # p.ej. [{"Windows": 100, "MacOS": 120, "Linux": 110}]
```

## 3. Mapeo gráfica → esquema

| Familia | Gráficas | Esquema de `data` | Notas |
|---|---|---|---|
| Area | area_chart, area_chart_full, area_chart_gradient, area_chart_semi_filled | `list[TimePoint]` | Igual que line |
| Line (simple) | line_chart, line_chart_curved, line_chart_labels_curved, line_chart_step, line_chart_pulse, line_chart_full | `list[TimePoint]` | — |
| Line (stocks) | line_chart_stocks_curved | `list[TimePoint]` | Formato de eje tipo bolsa |
| Line (múltiple) | line_chart_multiple | `list[list[TimePoint]]` o props `data`, `data2` | Varias series (el original usa `sales`, `sales2`) |
| Bar (DIV/SVG) | las 12 bar_* | `list[BarItem]` | `key`+`value`; breakdown/benchmark añaden campos extra (ver §4) |
| Pie/Donut | pie_*, donut_* | `list[CategoryValue]` | `name`+`value`; paleta vía `colors` |
| Scatter | scatter_chart, scatter_chart_stocks | `list[ScatterPoint]` | `revenue`(x), `value`(y), `company` |
| Scatter multiclass | scatter_chart_multiclass | `list[ScatterPoint]` + `class` | Campo de clase para color |
| Scatter interactivo | scatter_chart_interactive | `list[ScatterPoint]` | Emite `on_point_click` |
| Treemap | treemap_chart, treemap_chart_images, treemap_chart_gradient | `list[TreemapNode]` | Anidado; images añade `img` por nodo |
| Radar | radar_chart, radar_chart_rounded | `list[RadarPoint]` | `topic`+`value` |
| Other | bubble_chart | `list[ScatterPoint]` + `size` | Burbuja = scatter con radio |
| Other | funnel_chart | `list[FunnelStage]` | Etapas ordenadas |

## 4. Variantes con campos adicionales

Algunas gráficas extienden el esquema base. Se documentarán con precisión al portarlas; previsión:

| Gráfica | Campos extra (previstos) |
|---|---|
| bar_chart_breakdown / bar_chart_thin_breakdown | series apiladas: `value` por segmento o lista de segmentos |
| bar_chart_benchmark | `value` + `benchmark` (línea de referencia) |
| bar_chart_line | `value` (barra) + `line` (serie superpuesta) |
| bar_chart_horizontal_logo / *_flags_* | `key`, `value` + `logo`/`flag` (URL de imagen) |
| treemap_chart_images | nodos con `img` (URL) |
| donut_chart_center_text | `data` + prop `center_text` |
| donut_chart_fillable / *_half | `value` (0–100) de relleno |

> Regla: cada variante define su `TypedDict` propio (extendiendo el base) en el módulo de la gráfica,
> y lo referencia el API Spec correspondiente.

## 5. Ejemplos por esquema (defaults del original)

```python
# TimePoint (line/area)
[{"date": "2023-05-01", "value": 6}, {"date": "2023-05-02", "value": 8}]

# BarItem (bar)
[{"key": "Technology", "value": 38.1}, {"key": "Financials", "value": 25.3}]

# CategoryValue (pie/donut)
[{"name": "AAPL", "value": 30}, {"name": "BTC", "value": 22}]

# ScatterPoint (scatter)
[{"revenue": 10, "value": 102.8, "company": "Company A"}]

# RadarPoint (radar)
[{"topic": "Tech", "value": 330}, {"topic": "Energy", "value": 140}]

# TreemapNode (treemap)
[{"topic": "Tech", "subtopics": [{"Windows": 100, "MacOS": 120, "Linux": 110}]}]
```

## 6. Validación

| Regla | Cómo se aplica |
|---|---|
| Tipos de campo | Tipado estático con `TypedDict` + `rx.Var[list[Schema]]` (compilación Reflex) |
| Lista vacía | Permitida → render de estado vacío |
| Claves desconocidas | Ignoradas por el TSX (sólo lee las que usa) |
| Fechas | String ISO; conversión a `Date` en el cliente |

---

## Historial de Cambios

| Versión | Fecha | Autor | Cambios |
|---|---|---|---|
| 1.0 | 2026-06-14 | Ernesto Crespo | Esquemas base y mapeo de las 43 gráficas |
