# SDD Specifications — reflex-rosencharts

This directory contains the project specifications following the
**Spec-Driven Design (SDD)** methodology: the specs are the primary artifact and are approved
*before* the code for each chart is written.

## SDD flow

```
PRD (The What) → API Spec (Python Contract) → Tech Design (The How) → Data Model → Implementation Plan (Phases)
```

## Document index

| # | Document | Path | Status |
|---|-----------|------|--------|
| 1 | Product Requirements Document | [prd/reflex-rosencharts-prd.md](prd/reflex-rosencharts-prd.md) | DRAFT |
| 2 | API Spec (library's public Python API) | [api/component-api-v1.md](api/component-api-v1.md) | DRAFT |
| 3 | Technical Design | [technical/architecture.md](technical/architecture.md) | DRAFT |
| 4 | Data Model (chart data schemas) | [data-model/chart-data-schemas.md](data-model/chart-data-schemas.md) | DRAFT |
| 5 | Implementation Plan (by phases) | [plans/implementation-plan.md](plans/implementation-plan.md) | DRAFT |

## Nature of the project

`reflex-rosencharts` is a **port** of the [rosencharts](https://github.com/Filsommer/rosenCharts)
library (43 chart components in React/TSX based on D3.js + Tailwind) to a **custom component
for [Reflex](https://reflex.dev/)** publishable on PyPI, so the charts can be used
from pure Python.

Since it is a component library (not a REST service), the SDD templates are adapted as follows:
- **API Spec** documents the public Python API (component functions, props, event handlers).
- **Data Model** documents the data schemas of each chart (`TypedDict` / `rx.PropsBase`).
- There are no HTTP endpoints, database, or queues; the corresponding sections are omitted or reinterpreted.
