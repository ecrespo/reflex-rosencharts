# reflex-rosencharts — Implementation Plan

## Metadata

| Campo | Valor |
|---|---|
| **Autor** | Ernesto Crespo |
| **Estado** | `DRAFT` |
| **Versión** | 1.0 |
| **Fecha** | 2026-06-14 |
| **PRD** | [../prd/reflex-rosencharts-prd.md](../prd/reflex-rosencharts-prd.md) |
| **Tech Design** | [../technical/architecture.md](../technical/architecture.md) |
| **Data Model** | [../data-model/chart-data-schemas.md](../data-model/chart-data-schemas.md) |
| **API Spec** | [../api/component-api-v1.md](../api/component-api-v1.md) |

---

## 1. Resumen de Implementación

Se portan las **43 gráficas** de rosencharts a Reflex en **8 fases** tras una fase de fundación.
Estrategia: primero resolver la infraestructura de wrapping (Tailwind + helper de tooltip + receta
repetible) sobre **una** gráfica de referencia; luego portar **por familias**, de la más simple
(menos campos, sin tooltip) a la más compleja (anidada/interactiva). Cada gráfica incluye su wrapper
Python, su TSX parametrizado, su página de ejemplo en la galería y sus tests.

**Duración total estimada:** 6-7 semanas (1 persona) · **Equipo:** 1 dev full-stack (Python+React).
**Gate de release:** 43/43 gráficas portadas, con ejemplo y compilando, antes de publicar a PyPI.

## 2. Pre-requisitos

| Pre-requisito | Owner | Estado | Notas |
|---|---|---|---|
| Specs SDD aprobados | Ernesto | ☐ | Este conjunto de documentos |
| Proyecto Reflex + uv inicializado | Ernesto | ✅ | Hecho en esta sesión |
| Repo GitHub creado | Ernesto | ☐ | Requiere `gh auth login` |
| Node/Bun disponible para `reflex run` | Ernesto | ☐ | Reflex gestiona Bun; verificar en entorno de dev |
| Decisión NoSSR por gráfica | Ernesto | ☐ | Confirmar en spike (F0) |

## 3. Fases de Implementación

---

### Fase 0: Fundación e Infraestructura de Wrapping

**Duración:** ~1 semana · **Objetivo:** Resolver Tailwind + tooltip + receta sobre 1 gráfica.

| ID | Tarea | Estimación | Dependencia | Estado |
|---|---|---|---|---|
| F0-01 | Estructura de paquete (`components/<familia>/`) y `__init__` | 0.5d | — | ✅ (scaffold) |
| F0-02 | Habilitar y validar **Tailwind** en `rxconfig.py` (spike) | 1d | F0-01 | ☐ |
| F0-03 | Portar helper **`ClientTooltip`** y validarlo en aislamiento | 1d | F0-02 | ☐ |
| F0-04 | Portar **`line_chart`** (gráfica piloto) end-to-end con la receta | 1.5d | F0-03 | ☐ |
| F0-05 | Parametrizar datos del piloto (prop `data` + default = ejemplo) | 0.5d | F0-04 | ☐ |
| F0-06 | Página de galería base + 1 ejemplo (piloto) | 0.5d | F0-04 | ☐ |
| F0-07 | Tests base (import + render) y workflow de comparación visual | 1d | F0-04 | ☐ |
| F0-08 | Documentar la **receta de port** definitiva en CONTRIBUTING | 0.5d | F0-04 | ☐ |

**Done:** `rxc.line_chart()` renderiza idéntico al original; Tailwind y tooltip funcionan; receta escrita.

---

### Fase 1: Familia Line (8 gráficas)

**Duración:** ~3-4 días · **Dep:** F0. Reutiliza la receta del piloto.

| ID | Gráfica | Notas | Estado |
|---|---|---|---|
| F1-01 | `line_chart` | piloto (de F0) | ☐ |
| F1-02 | `line_chart_curved` | curva D3 | ☐ |
| F1-03 | `line_chart_step` | step | ☐ |
| F1-04 | `line_chart_pulse` | animación de pulso | ☐ |
| F1-05 | `line_chart_labels_curved` | labels | ☐ |
| F1-06 | `line_chart_full` | ejes completos | ☐ |
| F1-07 | `line_chart_stocks_curved` | formato bolsa | ☐ |
| F1-08 | `line_chart_multiple` | **multi-serie** (`data`, `data2`) | ☐ |

**Done:** 8 funciones `line_*` + ejemplos + tests; comparación visual OK.

---

### Fase 2: Familia Area (4 gráficas)

**Duración:** ~2 días · **Dep:** F1 (mismo esquema `TimePoint`).

| ID | Gráfica | Notas | Estado |
|---|---|---|---|
| F2-01 | `area_chart` | base | ☐ |
| F2-02 | `area_chart_full` | ejes | ☐ |
| F2-03 | `area_chart_gradient` | gradiente SVG | ☐ |
| F2-04 | `area_chart_semi_filled` | relleno parcial | ☐ |

**Done:** 4 funciones `area_*` + ejemplos + tests.

---

### Fase 3: Familia Bar (12 gráficas)

**Duración:** ~1 semana · **Dep:** F0. Mezcla DIV y SVG; varias variantes con campos extra.

| ID | Gráfica | Técnica/Notas | Estado |
|---|---|---|---|
| F3-01 | `bar_chart_horizontal` | DIV | ☐ |
| F3-02 | `bar_chart_vertical` | DIV | ☐ |
| F3-03 | `bar_chart_thin_horizontal` | DIV | ☐ |
| F3-04 | `bar_chart_gradient` | DIV + gradiente | ☐ |
| F3-05 | `bar_chart_multi_vertical` | DIV multi-serie | ☐ |
| F3-06 | `bar_chart_horizontal_logo` | DIV + `logo` (imagen) | ☐ |
| F3-07 | `bar_chart_flags_horizontal` | SVG + `flag` | ☐ |
| F3-08 | `bar_chart_triple_flags_horizontal` | DIV + flags x3 | ☐ |
| F3-09 | `bar_chart_breakdown` | SVG apilado | ☐ |
| F3-10 | `bar_chart_thin_breakdown` | SVG apilado fino | ☐ |
| F3-11 | `bar_chart_line` | SVG barra + línea | ☐ |
| F3-12 | `bar_chart_benchmark` | SVG + `benchmark` | ☐ |

**Done:** 12 funciones `bar_*`; `TypedDict` de variantes documentados; ejemplos + tests.

---

### Fase 4: Familia Pie/Donut (8 gráficas)

**Duración:** ~3-4 días · **Dep:** F0. Paleta `colors`.

| ID | Gráfica | Notas | Estado |
|---|---|---|---|
| F4-01 | `pie_chart` | base | ☐ |
| F4-02 | `pie_chart_labels` | labels | ☐ |
| F4-03 | `pie_chart_stocks` | tema bolsa | ☐ |
| F4-04 | `donut_chart` | hueco central | ☐ |
| F4-05 | `donut_chart_center_text` | prop `center_text` | ☐ |
| F4-06 | `donut_chart_half` | semicírculo | ☐ |
| F4-07 | `donut_chart_fillable` | `value` 0–100 | ☐ |
| F4-08 | `donut_chart_fillable_half` | gauge | ☐ |

**Done:** 8 funciones `pie_*`/`donut_*` + ejemplos + tests.

---

### Fase 5: Familia Scatter (4 gráficas)

**Duración:** ~3 días · **Dep:** F0. Incluye **interactividad** (event handler).

| ID | Gráfica | Notas | Estado |
|---|---|---|---|
| F5-01 | `scatter_chart` | base | ☐ |
| F5-02 | `scatter_chart_stocks` | tema bolsa | ☐ |
| F5-03 | `scatter_chart_multiclass` | color por clase | ☐ |
| F5-04 | `scatter_chart_interactive` | `on_point_click` (EventHandler) | ☐ |

**Done:** 4 funciones `scatter_*`; event handler validado contra `rx.State`.

---

### Fase 6: Familias Treemap + Radar (5 gráficas)

**Duración:** ~3-4 días · **Dep:** F0. Treemap usa estructura **anidada**.

| ID | Gráfica | Notas | Estado |
|---|---|---|---|
| F6-01 | `treemap_chart` | DIV anidado | ☐ |
| F6-02 | `treemap_chart_gradient` | DIV + gradiente | ☐ |
| F6-03 | `treemap_chart_images` | nodos con `img` | ☐ |
| F6-04 | `radar_chart` | polígono | ☐ |
| F6-05 | `radar_chart_rounded` | aristas redondeadas | ☐ |

**Done:** 5 funciones + ejemplos + tests; esquema anidado de treemap validado.

---

### Fase 7: Familia Other (2 gráficas) + Galería completa

**Duración:** ~3 días · **Dep:** F1-F6.

| ID | Tarea | Notas | Estado |
|---|---|---|---|
| F7-01 | `bubble_chart` | scatter con radio | ☐ |
| F7-02 | `funnel_chart` | etapas | ☐ |
| F7-03 | Galería: navegación por familias + snippet por gráfica | 43 ejemplos | ☐ |
| F7-04 | Auditoría de paridad visual (43/43) por captura | gate de calidad | ☐ |
| F7-05 | Cobertura de tests Python > 70% | — | ☐ |

**Done:** 43/43 con ejemplo en galería; auditoría visual firmada.

---

### Fase 8: Empaquetado, Documentación y Publicación

**Duración:** ~2-3 días · **Dep:** F7.

| ID | Tarea | Notas | Estado |
|---|---|---|---|
| F8-01 | `pyproject.toml` de distribución (metadatos, clasificadores, incluir assets `.tsx`) | — | ☐ |
| F8-02 | README con instalación, quickstart y galería de snippets | — | ☐ |
| F8-03 | LICENSE MIT + atribución a rosencharts (Filsommer) | obligatorio | ☐ |
| F8-04 | CI (GitHub Actions): lint + tests + build | — | ☐ |
| F8-05 | Build del custom component (`reflex component build` / Hatch) | — | ☐ |
| F8-06 | Publicar `0.1.0` en PyPI (TestPyPI primero) | gate final | ☐ |

**Done:** `pip install reflex-rosencharts` funciona; CI verde; release etiquetado.

## 4. Mapa de Dependencias

```
Fase 0: Fundación (Tailwind + ClientTooltip + receta sobre line_chart)
   │
   ├──▶ Fase 1: Line ──▶ Fase 2: Area   (comparten TimePoint)
   ├──▶ Fase 3: Bar
   ├──▶ Fase 4: Pie/Donut
   ├──▶ Fase 5: Scatter (interactividad)
   └──▶ Fase 6: Treemap + Radar
                 │
                 ▼
        Fase 7: Other + Galería completa ──▶ Fase 8: Empaquetado y Publicación
```

Las fases 1-6 pueden paralelizarse si hay más de un desarrollador (todas dependen sólo de F0).

## 5. Riesgos de Implementación

| Riesgo | Prob. | Impacto | Mitigación | Owner |
|---|---|---|---|---|
| Tailwind no genera clases dinámicas | Media | Alto | Spike F0-02; safelist de clases necesarias | Ernesto |
| Errores de hidratación por portales (tooltip) | Media | Medio | `NoSSRComponent`/dynamic import en gráficas con tooltip | Ernesto |
| Variantes con campos extra rompen el esquema base | Media | Medio | `TypedDict` propio por variante (Data Model §4) | Ernesto |
| Paridad visual difícil en gráficas complejas | Media | Medio | Comparación por captura contra `reference/` | Ernesto |
| Empaquetar assets `.tsx` en el wheel | Baja | Alto | Configurar `include` de assets en build; probar en TestPyPI | Ernesto |

## 6. Seguimiento

- Tablero por fase con el estado `☐/✅` de cada gráfica (este documento es la fuente de verdad).
- Cada familia mergea cuando: compila + ejemplo en galería + tests verdes + revisión visual.

## 7. Definición de Done (Global, por gráfica)

- [ ] Wrapper Python implementado y re-exportado
- [ ] TSX parametrizado (datos por prop; default = ejemplo original)
- [ ] Página de ejemplo en la galería
- [ ] Tests (import + render) en verde; compila en build de Reflex
- [ ] Paridad visual revisada contra `reference/rosencharts/`
- [ ] Docstring con esquema de datos y snippet de uso

---

## Historial de Cambios

| Versión | Fecha | Autor | Cambios |
|---|---|---|---|
| 1.0 | 2026-06-14 | Ernesto Crespo | Plan por familias para las 43 gráficas |
