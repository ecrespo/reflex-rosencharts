# Especificaciones SDD — reflex-rosencharts

Este directorio contiene las especificaciones del proyecto siguiendo la metodología
**Spec-Driven Design (SDD)**: las specs son el artefacto primario y se aprueban *antes*
de escribir el código de cada gráfica.

## Flujo SDD

```
PRD (El Qué) → API Spec (Contrato Python) → Tech Design (El Cómo) → Data Model → Implementation Plan (Fases)
```

## Índice de documentos

| # | Documento | Ruta | Estado |
|---|-----------|------|--------|
| 1 | Product Requirements Document | [prd/reflex-rosencharts-prd.md](prd/reflex-rosencharts-prd.md) | DRAFT |
| 2 | API Spec (API pública Python de la librería) | [api/component-api-v1.md](api/component-api-v1.md) | DRAFT |
| 3 | Technical Design | [technical/architecture.md](technical/architecture.md) | DRAFT |
| 4 | Data Model (esquemas de datos de las gráficas) | [data-model/chart-data-schemas.md](data-model/chart-data-schemas.md) | DRAFT |
| 5 | Implementation Plan (por fases) | [plans/implementation-plan.md](plans/implementation-plan.md) | DRAFT |

## Naturaleza del proyecto

`reflex-rosencharts` es un **port** de la librería [rosencharts](https://github.com/Filsommer/rosenCharts)
(43 componentes de gráficas en React/TSX basados en D3.js + Tailwind) a un **custom component
de [Reflex](https://reflex.dev/)** publicable en PyPI, de modo que se puedan usar las gráficas
desde Python puro.

Como es una librería de componentes (no un servicio REST), las plantillas SDD se adaptan así:
- **API Spec** documenta la API pública de Python (funciones de componente, props, event handlers).
- **Data Model** documenta los esquemas de datos de cada gráfica (`TypedDict` / `rx.PropsBase`).
- No hay endpoints HTTP, base de datos ni colas; las secciones correspondientes se omiten o reinterpretan.
