# reflex-rosencharts — API Specification (API pública Python)

## Metadata

| Campo | Valor |
|---|---|
| **Autor** | Ernesto Crespo |
| **Estado** | `DRAFT` |
| **Versión API** | v1.0 |
| **Fecha** | 2026-06-14 |
| **PRD Relacionado** | [../prd/reflex-rosencharts-prd.md](../prd/reflex-rosencharts-prd.md) |
| **Paquete** | `reflex_rosencharts` (alias sugerido `rxc`) |

---

> **Nota de adaptación SDD:** Esta no es una API HTTP. El "contrato" de esta librería es su
> **API pública de Python**: las funciones de componente, sus props, tipos y event handlers.
> Las secciones de auth/rate-limit/webhooks de la plantilla original no aplican y se omiten.

## 1. Visión General

La librería expone una función por gráfica que retorna un `rx.Component`. El consumidor importa el
paquete y compone las gráficas en sus páginas Reflex, alimentándolas con datos desde `rx.State`.

```python
import reflex as rx
import reflex_rosencharts as rxc

class State(rx.State):
    sales: list[dict] = [{"date": "2023-05-01", "value": 6}, {"date": "2023-05-02", "value": 8}]

def index() -> rx.Component:
    return rxc.line_chart(data=State.sales, height="18rem")
```

## 2. Convenciones de la API

### 2.1 Nomenclatura
- Una función pública por gráfica, en `snake_case`, derivada del nombre original:
  `1_LineChart.tsx` → `line_chart`, `5_DonutChartCenterText.tsx` → `donut_chart_center_text`.
- Re-exportadas desde `reflex_rosencharts/__init__.py`.
- Variantes "_DIV" (basadas en `<div>` en vez de SVG) conservan el nombre semántico sin el sufijo
  `_DIV` (p. ej. `bar_chart_horizontal`), documentando internamente la técnica de render.

### 2.2 Props comunes (todas las gráficas)

| Prop | Tipo | Default | Descripción |
|---|---|---|---|
| `data` | `rx.Var[list[dict]]` | `[]` | Conjunto de datos de la serie. Esquema según el tipo (ver Data Model). |
| `height` | `rx.Var[str]` | `"18rem"` (`h-72`) | Alto del contenedor (CSS). |
| `width` | `rx.Var[str]` | `"100%"` | Ancho del contenedor. |
| `class_name` | `rx.Var[str]` | `""` | Clases Tailwind extra para el contenedor raíz. |

### 2.3 Props de color / paleta (donde aplica)

| Prop | Tipo | Default | Descripción |
|---|---|---|---|
| `color` | `rx.Var[str]` | clase original | Color principal (clase Tailwind o valor CSS). |
| `colors` | `rx.Var[list[str]]` | paleta original | Paleta para series múltiples (pie, multiline, multibar, scatter multiclass). |
| `gradient` | `rx.Var[bool]` | según variante | Activa relleno con gradiente (variantes gradient). |

### 2.4 Event Handlers (gráficas interactivas)

| Handler | Spec | Gráficas |
|---|---|---|
| `on_point_hover` | `rx.EventHandler[rx.event.passthrough_event_spec(dict)]` | Las 29 con `ClientTooltip` |
| `on_point_click` | `rx.EventHandler[rx.event.passthrough_event_spec(dict)]` | `scatter_chart_interactive`, charts con selección |

### 2.5 Tipado de datos
- Los esquemas de cada gráfica se definen con `TypedDict` (interop directo con la estructura JS) o
  `rx.PropsBase` cuando se requiere conversión automática a camelCase. Detalle en el Data Model.
- Errores de tipo se detectan en tiempo de compilación de Reflex (no en runtime HTTP).

## 3. Catálogo de componentes (43)

Estado por defecto: `☐ Pendiente` (se actualiza al portar cada uno).

### 3.1 Area (`reflex_rosencharts.components.area`)

| Función | Origen | Datos | Tooltip | Estado |
|---|---|---|---|---|
| `area_chart` | area-charts/1_AreaChart.tsx | serie temporal | sí | ☐ |
| `area_chart_full` | area-charts/2_AreaChartFull.tsx | serie temporal | sí | ☐ |
| `area_chart_gradient` | area-charts/3_AreaChartGradient.tsx | serie temporal | sí | ☐ |
| `area_chart_semi_filled` | area-charts/4_AreaChartSemiFilled.tsx | serie temporal | sí | ☐ |

### 3.2 Bar (`reflex_rosencharts.components.bar`)

| Función | Origen | Técnica | Estado |
|---|---|---|---|
| `bar_chart_horizontal` | bar-charts/1_BarChartHorizontal_DIV.tsx | DIV | ☐ |
| `bar_chart_horizontal_logo` | bar-charts/2_BarChartHorizontalLogo_DIV.tsx | DIV | ☐ |
| `bar_chart_gradient` | bar-charts/3_BarChartGradient_DIV.tsx | DIV | ☐ |
| `bar_chart_breakdown` | bar-charts/4_BarChartBreakdown.tsx | SVG | ☐ |
| `bar_chart_thin_breakdown` | bar-charts/5_BarChartThinBreakdown.tsx | SVG | ☐ |
| `bar_chart_thin_horizontal` | bar-charts/6_BarChartThinHorizontal_DIV.tsx | DIV | ☐ |
| `bar_chart_flags_horizontal` | bar-charts/7_BarChartFlagsHorizontal.tsx | SVG | ☐ |
| `bar_chart_vertical` | bar-charts/9_BarChartVertical_DIV.tsx | DIV | ☐ |
| `bar_chart_multi_vertical` | bar-charts/11_BarChartMultiVertical_DIV.tsx | DIV | ☐ |
| `bar_chart_triple_flags_horizontal` | bar-charts/12_BarChartTripleFlagsHorizontal_DIV.tsx | DIV | ☐ |
| `bar_chart_line` | bar-charts/14_BarChartLine.tsx | SVG | ☐ |
| `bar_chart_benchmark` | bar-charts/15_BarChartBenchmark.tsx | SVG | ☐ |

### 3.3 Line (`reflex_rosencharts.components.line`)

| Función | Origen | Estado |
|---|---|---|
| `line_chart` | line-charts/1_LineChart.tsx | ☐ |
| `line_chart_curved` | line-charts/2_LineChartCurved.tsx | ☐ |
| `line_chart_multiple` | line-charts/3_LineChartMultiple.tsx | ☐ |
| `line_chart_labels_curved` | line-charts/4_LineChartLabelsCurved.tsx | ☐ |
| `line_chart_stocks_curved` | line-charts/5_LineChartStocksCurved.tsx | ☐ |
| `line_chart_step` | line-charts/6_LineChartStep.tsx | ☐ |
| `line_chart_pulse` | line-charts/7_LineChartPulse.tsx | ☐ |
| `line_chart_full` | line-charts/8_LineChartFull.tsx | ☐ |

### 3.4 Pie / Donut (`reflex_rosencharts.components.pie`)

| Función | Origen | Estado |
|---|---|---|
| `pie_chart` | pie-charts/1_PieChart.tsx | ☐ |
| `pie_chart_stocks` | pie-charts/2_PieChartStocks.tsx | ☐ |
| `pie_chart_labels` | pie-charts/3_PieChartLabels.tsx | ☐ |
| `donut_chart` | pie-charts/4_DonutChart.tsx | ☐ |
| `donut_chart_center_text` | pie-charts/5_DonutChartCenterText.tsx | ☐ |
| `donut_chart_half` | pie-charts/6_DonutChartHalf.tsx | ☐ |
| `donut_chart_fillable_half` | pie-charts/7_DonutChartFillableHalf.tsx | ☐ |
| `donut_chart_fillable` | pie-charts/8_DonutChartFillable.tsx | ☐ |

### 3.5 Scatter (`reflex_rosencharts.components.scatter`)

| Función | Origen | Interactiva | Estado |
|---|---|---|---|
| `scatter_chart` | scatter-charts/1_ScatterChart.tsx | no | ☐ |
| `scatter_chart_interactive` | scatter-charts/2_ScatterChartInteractive.tsx | sí | ☐ |
| `scatter_chart_multiclass` | scatter-charts/5_ScatterChartMulticlass.tsx | no | ☐ |
| `scatter_chart_stocks` | scatter-charts/6_ScatterChartStocks.tsx | no | ☐ |

### 3.6 Treemap (`reflex_rosencharts.components.treemap`)

| Función | Origen | Estado |
|---|---|---|
| `treemap_chart` | treemap-charts/1_TreemapChart_DIV.tsx | ☐ |
| `treemap_chart_images` | treemap-charts/2_TreemapChartImages_DIV.tsx | ☐ |
| `treemap_chart_gradient` | treemap-charts/3_TreemapChartGradient_DIV.tsx | ☐ |

### 3.7 Radar (`reflex_rosencharts.components.radar`)

| Función | Origen | Estado |
|---|---|---|
| `radar_chart` | radar-charts/6_RadarChart.tsx | ☐ |
| `radar_chart_rounded` | radar-charts/8_RadarChartRounded.tsx | ☐ |

### 3.8 Other (`reflex_rosencharts.components.other`)

| Función | Origen | Estado |
|---|---|---|
| `bubble_chart` | other-charts/4_BubbleChart_DIV.tsx | ☐ |
| `funnel_chart` | other-charts/5_FunnelChart.tsx | ☐ |

## 4. Especificación detallada (ejemplos representativos)

### 4.1 `line_chart(data, *, height, width, color, class_name, on_point_hover)`

**Descripción:** Gráfica de línea sobre serie temporal con tooltip por punto.

**Props:**

| Prop | Tipo | Requerido | Regla | Default |
|---|---|---|---|---|
| `data` | `list[LinePoint]` | Sí | lista no vacía de `{date, value}` | `[]` |
| `color` | `str` | No | clase Tailwind (`stroke-*`) o color | `"stroke-fuchsia-400"` |
| `height` | `str` | No | CSS válido | `"18rem"` |
| `on_point_hover` | EventHandler | No | recibe `{date, value}` | — |

**Tipo de dato (`LinePoint`):**
```python
class LinePoint(TypedDict):
    date: str    # ISO date 'YYYY-MM-DD'
    value: float
```

**Ejemplo de uso:**
```python
rxc.line_chart(
    data=State.sales,            # [{"date": "2023-05-01", "value": 6}, ...]
    color="stroke-indigo-500",
    height="20rem",
    on_point_hover=State.handle_hover,
)
```

### 4.2 `donut_chart(data, *, height, colors, class_name)`

**Tipo de dato (`CategoryValue`):**
```python
class CategoryValue(TypedDict):
    name: str
    value: float
```

**Ejemplo:**
```python
rxc.donut_chart(
    data=[{"name": "AAPL", "value": 38}, {"name": "MSFT", "value": 22}],
    colors=["#6366f1", "#22c55e", "#f59e0b"],
)
```

### 4.3 `scatter_chart_interactive(data, *, on_point_click, ...)`

**Tipo de dato (`ScatterPoint`):**
```python
class ScatterPoint(TypedDict):
    x: float
    y: float
    label: str  # opcional según gráfica
```

**Event handler:** `on_point_click` recibe el punto `{x, y, label}` al hacer clic.

## 5. Errores y validación

| Situación | Comportamiento esperado |
|---|---|
| `data` vacío | Render de estado vacío (sin error); la gráfica no dibuja series. |
| Esquema de dato incorrecto | Error de tipado en compilación de Reflex / log en consola. |
| Prop de color inválido | Se aplica tal cual a la clase/estilo; degradación visual, sin crash. |

## 6. Versionado

- Versionado semántico del paquete (`MAJOR.MINOR.PATCH`).
- v1.x: API estable de las funciones listadas. Cambios incompatibles → v2.

---

## Historial de Cambios

| Versión | Fecha | Cambios |
|---|---|---|
| 1.0 | 2026-06-14 | Catálogo inicial de las 43 funciones y props comunes |
