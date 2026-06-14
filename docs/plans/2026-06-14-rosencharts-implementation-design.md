# reflex-rosencharts — Execution design (port of the 43 charts)

| Field | Value |
|---|---|
| **Author** | Ernesto Crespo (with Claude) |
| **Date** | 2026-06-14 |
| **Status** | Approved (brainstorming) |
| **Base specs** | [PRD](../../specs/prd/reflex-rosencharts-prd.md) · [Tech Design](../../specs/technical/architecture.md) · [API](../../specs/api/component-api-v1.md) · [Data Model](../../specs/data-model/chart-data-schemas.md) · [Plan](../../specs/plans/implementation-plan.md) |

> The **architecture** (wrapping with `rx.asset` + `library="$/public..."`, data parameterization,
> Tailwind, tooltip/SSR) is already fixed in the SDD specs. This document defines **how the port
> of the 43 charts is executed** in one session, with TDD and verification.

## 1. Session decisions (approved)

| Decision | Value |
|---|---|
| **Scope** | The full **43 charts** + demo gallery |
| **Methodology** | **TDD** across the entire Python layer (red → green → refactor per chart) |
| **Execution** | Recipe proven in the pilot by the lead dev → **multi-agent workflow** by families for the remaining 42 |
| **Verification** | Green pytest tests + `reflex run` compiles the gallery + **Playwright screenshots** vs `reference/` |

## 2. Guiding principle

Agents are not fanned out over an unproven recipe. First the full path is proven
(Tailwind + D3 + ClientTooltip + wrapping + demo) on **1 pilot chart** and it is verified that it
**compiles and renders**; only then is the rest parallelized.

## 3. Stages

### Stage A — Foundation + pilot (sequential, verified, TDD)

1. Port `ClientTooltip.tsx` into the package as a shared helper; NoSSR wrapper (uses `createPortal`).
2. Resolve Tailwind V4: ensure the TSX classes are scanned/generated. Define a **safelist**
   for dynamic classes that arrive via prop (e.g. `stroke-fuchsia-400`, palettes).
3. Declare the npm dependency **`d3`** in the wrapper (`lib_dependencies`).
4. **TDD `line_chart`** (pilot): test first (exists, importable, `.create(data=...)` → `rx.Component`
   with correct `tag`/`library`/props, default = example) → parameterized TSX + Python wrapper → green.
5. Set up the **demo gallery** (sidebar by family, card + snippet per chart) with the pilot and
   **verify that `reflex run` / export compiles** without TSX/Tailwind errors.

**Stage A exit gate:** `rxc.line_chart()` renders identically to the original; green tests; compiles.

### Stage B — Fan-out of the remaining 42 (multi-agent workflow by family)

- Pipeline by family: line (rest), area, bar, pie/donut, scatter, treemap, radar, other.
- Each agent receives: the **proven recipe** (from Stage A), the reference TSX, and the data schema.
  It ports its chart **following TDD** (test → wrapper + parameterized TSX → green), isolated in its module,
  and re-exports it.
- The families run in parallel (they all depend only on the foundation).

### Stage C — Integration + verification

- Collect wrappers; run the **full pytest suite** (green, Python coverage > 70%).
- Complete the gallery with all 43; **verify that the app compiles** (`reflex run`/export) without errors.
- **Playwright screenshots** of each chart to compare against `reference/` (visual parity audit
  by family).

## 4. File structure (Tech Design §5.1)

```
reflex_rosencharts/components/<family>/<name>.tsx   # parameterized TSX (default = example)
reflex_rosencharts/components/<family>/<name>.py    # rx.Component wrapper + public function
reflex_rosencharts/components/helpers/ClientTooltip.tsx + .py
reflex_rosencharts/__init__.py                       # re-export of the 43 functions
reflex_rosencharts/reflex_rosencharts.py             # demo gallery
tests/test_imports.py                                # smoke: all importable
tests/test_<family>.py                              # TDD per family (render/props)
```

## 5. Port recipe per chart (TDD)

```
RED   → test_<family>.py: the function exists, is importable, .create(data=...) builds
         an rx.Component with correct tag/library/props; default reproduces the example.
GREEN → 1. Copy reference/.../<n>_<Name>.tsx → components/<fam>/<name>.tsx
         2. Replace hardcoded data with the `data` prop (default = original example)
         3. Adjust the helper import to the local path
         4. Write the Python wrapper (rx.asset, library, tag, typed props; NoSSR if it uses a portal)
         5. Re-export in components/<fam>/__init__.py and in reflex_rosencharts/__init__.py
         6. Add an example page/card to the gallery
REFACTOR → clean up while keeping it green.
```

## 6. Risks and mitigations (from the session)

| Risk | Mitigation |
|---|---|
| Tailwind V4 does not generate dynamic classes from props | Safelist in config; proven in the pilot before the fan-out |
| Hydration from portals (tooltip) | `NoSSRComponent` / dynamic import in charts with a tooltip |
| Agents diverge from the recipe | Recipe proven and verified in Stage A before the fan-out; each agent receives it verbatim |
| Visual parity hard to auto-verify | Playwright screenshots vs `reference/`; final manual review with the demo |

## 7. Definition of Done (global)

- [ ] 43 Python wrappers + parameterized TSX, re-exported.
- [ ] Green pytest tests (TDD), Python coverage > 70%.
- [ ] Demo gallery with all 43 (card + snippet) and `reflex run` compiles.
- [ ] Playwright screenshots of all 43 vs `reference/`.
