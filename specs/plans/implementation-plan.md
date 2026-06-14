# reflex-rosencharts — Implementation Plan

## Metadata

| Field | Value |
|---|---|
| **Author** | Ernesto Crespo |
| **Status** | `DRAFT` |
| **Version** | 1.0 |
| **Date** | 2026-06-14 |
| **PRD** | [../prd/reflex-rosencharts-prd.md](../prd/reflex-rosencharts-prd.md) |
| **Tech Design** | [../technical/architecture.md](../technical/architecture.md) |
| **Data Model** | [../data-model/chart-data-schemas.md](../data-model/chart-data-schemas.md) |
| **API Spec** | [../api/component-api-v1.md](../api/component-api-v1.md) |

---

## 1. Implementation Summary

The **43 charts** from rosencharts are ported to Reflex across **8 phases** following a foundation phase.
Strategy: first resolve the wrapping infrastructure (Tailwind + tooltip helper + repeatable recipe)
on **one** reference chart; then port **by family**, from the simplest (fewest fields, no tooltip)
to the most complex (nested/interactive). Each chart includes its Python wrapper, its parameterized
TSX, its example page in the gallery, and its tests.

**Total estimated duration:** 6-7 weeks (1 person) · **Team:** 1 full-stack dev (Python+React).
**Release gate:** 43/43 charts ported, with example and compiling, before publishing to PyPI.

## 2. Prerequisites

| Prerequisite | Owner | Status | Notes |
|---|---|---|---|
| SDD specs approved | Ernesto | ☐ | This set of documents |
| Reflex + uv project initialized | Ernesto | ✅ | Done in this session |
| GitHub repo created | Ernesto | ☐ | Requires `gh auth login` |
| Node/Bun available for `reflex run` | Ernesto | ☐ | Reflex manages Bun; verify in dev environment |
| Per-chart NoSSR decision | Ernesto | ☐ | Confirm in spike (F0) |

## 3. Implementation Phases

---

### Phase 0: Foundation and Wrapping Infrastructure

**Duration:** ~1 week · **Goal:** Resolve Tailwind + tooltip + recipe on 1 chart.

| ID | Task | Estimate | Dependency | Status |
|---|---|---|---|---|
| F0-01 | Package structure (`components/<family>/`) and `__init__` | 0.5d | — | ✅ (scaffold) |
| F0-02 | Enable and validate **Tailwind** in `rxconfig.py` (spike) | 1d | F0-01 | ☐ |
| F0-03 | Port the **`ClientTooltip`** helper and validate it in isolation | 1d | F0-02 | ☐ |
| F0-04 | Port **`line_chart`** (pilot chart) end-to-end with the recipe | 1.5d | F0-03 | ☐ |
| F0-05 | Parameterize pilot data (`data` prop + default = example) | 0.5d | F0-04 | ☐ |
| F0-06 | Base gallery page + 1 example (pilot) | 0.5d | F0-04 | ☐ |
| F0-07 | Base tests (import + render) and visual comparison workflow | 1d | F0-04 | ☐ |
| F0-08 | Document the definitive **port recipe** in CONTRIBUTING | 0.5d | F0-04 | ☐ |

**Done:** `rxc.line_chart()` renders identically to the original; Tailwind and tooltip work; recipe written.

---

### Phase 1: Line Family (8 charts)

**Duration:** ~3-4 days · **Dep:** F0. Reuses the pilot recipe.

| ID | Chart | Notes | Status |
|---|---|---|---|
| F1-01 | `line_chart` | pilot (from F0) | ☐ |
| F1-02 | `line_chart_curved` | D3 curve | ☐ |
| F1-03 | `line_chart_step` | step | ☐ |
| F1-04 | `line_chart_pulse` | pulse animation | ☐ |
| F1-05 | `line_chart_labels_curved` | labels | ☐ |
| F1-06 | `line_chart_full` | full axes | ☐ |
| F1-07 | `line_chart_stocks_curved` | stock format | ☐ |
| F1-08 | `line_chart_multiple` | **multi-series** (`data`, `data2`) | ☐ |

**Done:** 8 `line_*` functions + examples + tests; visual comparison OK.

---

### Phase 2: Area Family (4 charts)

**Duration:** ~2 days · **Dep:** F1 (same `TimePoint` schema).

| ID | Chart | Notes | Status |
|---|---|---|---|
| F2-01 | `area_chart` | base | ☐ |
| F2-02 | `area_chart_full` | axes | ☐ |
| F2-03 | `area_chart_gradient` | SVG gradient | ☐ |
| F2-04 | `area_chart_semi_filled` | partial fill | ☐ |

**Done:** 4 `area_*` functions + examples + tests.

---

### Phase 3: Bar Family (12 charts)

**Duration:** ~1 week · **Dep:** F0. Mixes DIV and SVG; several variants with extra fields.

| ID | Chart | Technique/Notes | Status |
|---|---|---|---|
| F3-01 | `bar_chart_horizontal` | DIV | ☐ |
| F3-02 | `bar_chart_vertical` | DIV | ☐ |
| F3-03 | `bar_chart_thin_horizontal` | DIV | ☐ |
| F3-04 | `bar_chart_gradient` | DIV + gradient | ☐ |
| F3-05 | `bar_chart_multi_vertical` | DIV multi-series | ☐ |
| F3-06 | `bar_chart_horizontal_logo` | DIV + `logo` (image) | ☐ |
| F3-07 | `bar_chart_flags_horizontal` | SVG + `flag` | ☐ |
| F3-08 | `bar_chart_triple_flags_horizontal` | DIV + flags x3 | ☐ |
| F3-09 | `bar_chart_breakdown` | stacked SVG | ☐ |
| F3-10 | `bar_chart_thin_breakdown` | thin stacked SVG | ☐ |
| F3-11 | `bar_chart_line` | SVG bar + line | ☐ |
| F3-12 | `bar_chart_benchmark` | SVG + `benchmark` | ☐ |

**Done:** 12 `bar_*` functions; documented variant `TypedDict`s; examples + tests.

---

### Phase 4: Pie/Donut Family (8 charts)

**Duration:** ~3-4 days · **Dep:** F0. `colors` palette.

| ID | Chart | Notes | Status |
|---|---|---|---|
| F4-01 | `pie_chart` | base | ☐ |
| F4-02 | `pie_chart_labels` | labels | ☐ |
| F4-03 | `pie_chart_stocks` | stock theme | ☐ |
| F4-04 | `donut_chart` | center hole | ☐ |
| F4-05 | `donut_chart_center_text` | `center_text` prop | ☐ |
| F4-06 | `donut_chart_half` | semicircle | ☐ |
| F4-07 | `donut_chart_fillable` | `value` 0–100 | ☐ |
| F4-08 | `donut_chart_fillable_half` | gauge | ☐ |

**Done:** 8 `pie_*`/`donut_*` functions + examples + tests.

---

### Phase 5: Scatter Family (4 charts)

**Duration:** ~3 days · **Dep:** F0. Includes **interactivity** (event handler).

| ID | Chart | Notes | Status |
|---|---|---|---|
| F5-01 | `scatter_chart` | base | ☐ |
| F5-02 | `scatter_chart_stocks` | stock theme | ☐ |
| F5-03 | `scatter_chart_multiclass` | color per class | ☐ |
| F5-04 | `scatter_chart_interactive` | `on_point_click` (EventHandler) | ☐ |

**Done:** 4 `scatter_*` functions; event handler validated against `rx.State`.

---

### Phase 6: Treemap + Radar Families (5 charts)

**Duration:** ~3-4 days · **Dep:** F0. Treemap uses a **nested** structure.

| ID | Chart | Notes | Status |
|---|---|---|---|
| F6-01 | `treemap_chart` | nested DIV | ☐ |
| F6-02 | `treemap_chart_gradient` | DIV + gradient | ☐ |
| F6-03 | `treemap_chart_images` | nodes with `img` | ☐ |
| F6-04 | `radar_chart` | polygon | ☐ |
| F6-05 | `radar_chart_rounded` | rounded edges | ☐ |

**Done:** 5 functions + examples + tests; treemap nested schema validated.

---

### Phase 7: Other Family (2 charts) + Complete Gallery

**Duration:** ~3 days · **Dep:** F1-F6.

| ID | Task | Notes | Status |
|---|---|---|---|
| F7-01 | `bubble_chart` | scatter with radius | ☐ |
| F7-02 | `funnel_chart` | stages | ☐ |
| F7-03 | Gallery: navigation by family + snippet per chart | 43 examples | ☐ |
| F7-04 | Visual parity audit (43/43) by capture | quality gate | ☐ |
| F7-05 | Python test coverage > 70% | — | ☐ |

**Done:** 43/43 with example in the gallery; visual audit signed off.

---

### Phase 8: Packaging, Documentation, and Publication

**Duration:** ~2-3 days · **Dep:** F7.

| ID | Task | Notes | Status |
|---|---|---|---|
| F8-01 | Distribution `pyproject.toml` (metadata, classifiers, include `.tsx` assets) | — | ☐ |
| F8-02 | README with installation, quickstart, and snippet gallery | — | ☐ |
| F8-03 | MIT LICENSE + attribution to rosencharts (Filsommer) | mandatory | ☐ |
| F8-04 | CI (GitHub Actions): lint + tests + build | — | ☐ |
| F8-05 | Custom component build (`reflex component build` / Hatch) | — | ☐ |
| F8-06 | Publish `0.1.0` to PyPI (TestPyPI first) | final gate | ☐ |

**Done:** `pip install reflex-rosencharts` works; CI green; release tagged.

## 4. Dependency Map

```
Phase 0: Foundation (Tailwind + ClientTooltip + recipe on line_chart)
   │
   ├──▶ Phase 1: Line ──▶ Phase 2: Area   (share TimePoint)
   ├──▶ Phase 3: Bar
   ├──▶ Phase 4: Pie/Donut
   ├──▶ Phase 5: Scatter (interactivity)
   └──▶ Phase 6: Treemap + Radar
                 │
                 ▼
        Phase 7: Other + Complete Gallery ──▶ Phase 8: Packaging and Publication
```

Phases 1-6 can be parallelized if there is more than one developer (all depend only on F0).

## 5. Implementation Risks

| Risk | Prob. | Impact | Mitigation | Owner |
|---|---|---|---|---|
| Tailwind does not generate dynamic classes | Medium | High | Spike F0-02; safelist of required classes | Ernesto |
| Hydration errors from portals (tooltip) | Medium | Medium | `NoSSRComponent`/dynamic import in charts with tooltip | Ernesto |
| Variants with extra fields break the base schema | Medium | Medium | Dedicated `TypedDict` per variant (Data Model §4) | Ernesto |
| Visual parity hard on complex charts | Medium | Medium | Capture comparison against `reference/` | Ernesto |
| Packaging `.tsx` assets in the wheel | Low | High | Configure asset `include` in build; test on TestPyPI | Ernesto |

## 6. Tracking

- Per-phase board with the `☐/✅` status of each chart (this document is the source of truth).
- Each family merges when: compiles + example in gallery + tests green + visual review.

## 7. Definition of Done (Global, per chart)

- [ ] Python wrapper implemented and re-exported
- [ ] Parameterized TSX (data via prop; default = original example)
- [ ] Example page in the gallery
- [ ] Tests (import + render) green; compiles in Reflex build
- [ ] Visual parity reviewed against `reference/rosencharts/`
- [ ] Docstring with data schema and usage snippet

---

## Change History

| Version | Date | Author | Changes |
|---|---|---|---|
| 1.0 | 2026-06-14 | Ernesto Crespo | Family-based plan for the 43 charts |