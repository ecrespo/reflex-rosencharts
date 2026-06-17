# reflex-rosencharts — Technical Design Document

## Metadata

| Field | Value |
|---|---|
| **Author** | Ernesto Crespo |
| **Status** | `DRAFT` |
| **Version** | 1.0 |
| **Date** | 2026-06-14 |
| **Related PRD** | [../prd/reflex-rosencharts-prd.md](../prd/reflex-rosencharts-prd.md) |
| **Related API Spec** | [../api/component-api-v1.md](../api/component-api-v1.md) |

---

## 1. Context

rosencharts is a set of 43 React components written in TypeScript (`.tsx`) that use **D3.js**
for scale/path calculations and **Tailwind CSS** for styling. It is not an npm package: it is
distributed as copy-and-paste code, with **hardcoded data** inside each component and
a local helper `ClientTooltip.tsx` (used by 29 of the 43 charts) that renders the tooltip with
`createPortal` from `react-dom`.

Reflex allows **wrapping local React components**: with `rx.asset(...)` it copies the source file to the
generated frontend and, by declaring `library = f"$/public{ruta}"` and `tag`, exposes the component as an
`rx.Component` class with typed props. The core technical challenge is threefold: (1) **parametrizing** the
TSX so they receive data via props instead of having it hardcoded, (2) **integrating Tailwind** into
Reflex's build pipeline, and (3) handling the **tooltip with portals** (SSR) correctly.

This document defines the repeatable port pattern, the project structure, and the key decisions.

## 2. Technical Goals

- **Correctness:** each ported chart must be visually equivalent to its original with the same data.
- **Repeatability:** one "recipe" per category that a contributor can follow mechanically.
- **Maintainability:** small, isolated Python wrappers; parametrized TSX versioned alongside the wrapper; test coverage > 70% of the Python.
- **Operability:** the demo app serves as a visual test bench (one page per chart).

## 3. Proposed Architecture

### 3.1 High-Level Diagram

```
┌──────────────────────┐      ┌──────────────────────────┐      ┌───────────────────────┐
│  Reflex App (Python) │      │  reflex_rosencharts (pkg) │      │  Generated frontend    │
│  rx.State + pages     │────▶│  component functions      │────▶│  (.web): React + D3    │
│  data: list[dict]     │ data │  rx.Component + rx.asset   │ TSX  │  + Tailwind + Portals  │
└──────────────────────┘      └──────────────────────────┘      └───────────────────────┘
         │ props (data, color, height)                                   │ render SVG/DIV
         └───────────────────────────────────────────────────────────────┘
```

### 3.2 Components

| Component | Technology | Responsibility |
|---|---|---|
| Python wrappers | Python 3.13 / Reflex `rx.Component` | Declare `library/tag`, typed props, event handlers; public function per chart |
| Parametrized TSX | TypeScript / React / D3 | Render the chart receiving `props` (data, color, dimensions) |
| `ClientTooltip` helper | TSX / react-dom | Portal-based tooltip, shared by 29 charts |
| Tailwind integration | Reflex Tailwind plugin | Process utility classes used by the TSX |
| Demo app / gallery | Reflex | One example page per chart (the "examples folder") |
| Packaging | `reflex component` / `uv` / Hatch | Build and publish the custom component |

### 3.3 Data Flow

**Flow: rendering a chart**
```
1. The page calls rxc.line_chart(data=State.sales)
2. The Python wrapper creates the rx.Component with the `data` prop (rx.Var) and the other props
3. Reflex copies the local TSX to the frontend (rx.asset, shared=True) and generates the import from $/public
4. On the client, React mounts the TSX component and passes `data` as a prop
5. D3 computes scales and paths from `data`
6. SVG/DIV is rendered with Tailwind classes; ClientTooltip mounts the tooltip via portal on hover
```

**Error / degradation flow:**
```
1. empty data → the TSX early-returns an empty container (no throw)
2. unexpected schema → typing failure at Reflex compile time (never reaches runtime)
3. Tailwind failure (class not generated) → visual degradation, no crash
4. Portal/SSR → portal components mount client-side (NoSSR/dynamic) to avoid hydration errors
```

## 4. Design Decisions

### DD-001: Wrapping strategy — local components vs. publishing an intermediate npm

- **Decision:** Wrap the TSX as **local components** with `rx.asset` + `library="$/public..."`.
- **Context:** rosencharts is not an npm package; its components are loose TSX with embedded data.
- **Evaluated alternatives:**

| Option | Pros | Cons |
|---|---|---|
| **A. Local components (`rx.asset`) (chosen)** | No npm publishing; the TSX travels with the Python package; full control to parametrize | Each TSX must be parametrized; assets/CSS management |
| B. Publish an npm package `rosencharts-react` and wrap by `library` | "Standard" wrapping by package name | Maintain and publish an extra npm; build step; out of scope |
| C. Rewrite each chart in pure Python (no React/D3) | No JS dependency | Enormous effort; loses visual parity; reinvents D3 |

- **Rationale:** Option A delivers visual parity with the original with the minimum of infrastructure and keeps everything inside the Python package.
- **Consequences:** The package includes the parametrized `.tsx` as assets; JS is versioned inside the Python package.

### DD-002: Data parametrization

- **Decision:** Refactor each TSX so the hardcoded data becomes a **prop** (`data`, and chart-specific props), with defaults that reproduce the original example.
- **Context:** RF-002 requires feeding data from `rx.State`.
- **Consequences:** Each TSX gains a data default = the original example's dataset, so that `rxc.line_chart()` with no args reproduces the example.

### DD-003: Tailwind in Reflex

- **Decision:** Enable the Reflex Tailwind plugin and declare the TSX content so their classes are generated. Spike in Phase 1.
- **Alternatives:** (a) Tailwind plugin (chosen); (b) pre-compiled CSS attached via `rx.asset` (more fragile with dynamic classes).
- **Consequences:** The original Tailwind aesthetic is preserved without rewriting styles.

### DD-004: Tooltip / SSR

- **Decision:** Port `ClientTooltip` once as a shared helper; charts that use it are mounted client-side (dynamic import / `NoSSRComponent`) if hydration errors appear.
- **Consequences:** Tooltips identical to the original; zero SSR cost for those charts.

### DD-005: Name mapping and "_DIV"

- **Decision:** Semantic Python name in `snake_case`, dropping the `_DIV` suffix (a render technique, not part of the API). Document the technique in the docstring.
- **Consequences:** Clean, predictable API; the render technique remains an internal detail.

## 5. Patterns and Conventions

### 5.1 Code Structure

```
reflex-rosencharts/
├── specs/                          # SDD specifications (this set)
├── reference/rosencharts/          # Original TSX code (read-only, reference)
├── reflex_rosencharts/
│   ├── __init__.py                 # Re-exports all public functions
│   ├── reflex_rosencharts.py       # Demo app / gallery (example pages)
│   └── components/
│       ├── helpers/
│       │   ├── ClientTooltip.tsx   # ported helper (parametrized if applicable)
│       │   └── __init__.py
│       ├── area/
│       │   ├── area_chart.tsx      # parametrized TSX
│       │   ├── area_chart.py       # rx.Component wrapper + public function
│       │   └── __init__.py
│       ├── bar/  line/  pie/  scatter/  treemap/  radar/  other/
│       └── __init__.py
├── tests/
│   ├── test_imports.py             # smoke: all functions importable
│   └── test_components.py          # render/props per chart
├── rxconfig.py
├── pyproject.toml
└── README.md
```

### 5.2 Port recipe (repeatable pattern per chart)

```
1. Copy reference/rosencharts/<cat>/<n>_<Name>.tsx → reflex_rosencharts/components/<cat>/<name>.tsx
2. Replace the hardcoded `let data = [...]` with `export function Name({ data = <default>, ... }) `
3. Adjust the helper imports to the local path (./<...>/ClientTooltip)
4. Write the Python wrapper:
       path = rx.asset("./<name>.tsx", shared=True)
       class <Name>(rx.Component):           # or NoSSRComponent if it uses a portal
           library = f"$/public{path}"
           tag = "<Name>"; is_default = False
           data: rx.Var[list[<Schema>]] = rx.Var.create(<default>)
           # color/height/colors/event handlers per the API Spec
       def <name>(**props) -> rx.Component: return <Name>.create(**props)
5. Re-export in components/<cat>/__init__.py and in reflex_rosencharts/__init__.py
6. Add an example page to the gallery
7. Test: import + render; visual comparison via screenshot against the original
```

### 5.3 Applied Patterns

| Pattern | Where | Why |
|---|---|---|
| Wrapper per component | `components/<cat>/<name>.py` | Isolate each chart, independent evolution |
| Shared helper | `components/helpers/` | DRY the tooltip (29 charts) |
| Defaults = original example | Parametrized TSX | `func()` with no args reproduces the example |
| Subpackages per family | `components/<cat>/` | Organization and discoverability |

### 5.4 Error Handling
- No domain exceptions (there is no backend). The relevant failures are **compilation** (types/imports) and **styling** (Tailwind). Policy: empty data ⇒ empty render, never throw.

## 6. Security

| Vector | Mitigation |
|---|---|
| Injection via `data` into the DOM | D3/React escape text; no raw HTML is injected |
| JS dependencies (d3, react-dom) | Pinned versions; minimal surface |
| External assets (logos/images in variants) | URLs controlled by the consumer; document |

No sensitive data or credentials are handled: the library only renders data provided by the app.

## 7. Observability
- **Build:** TSX and Tailwind compilation errors visible in the `reflex run` console.
- **Runtime:** no built-in telemetry; the consumer instruments their app.

## 8. Testing Strategy

| Level | Target Coverage | Tools | What it covers |
|---|---|---|---|
| Unit (Python) | > 70% | pytest | That each function exists, is importable, and builds an `rx.Component` with props |
| Compilation | 100% of charts | `reflex export`/build | That each TSX compiles within Reflex |
| Visual | 43/43 | Captures (Playwright/manual) against `reference/` | Visual parity with the original |
| Smoke demo | 1 page/chart | Loading the gallery | That each example renders without error |

## 9. Migration / Rollout Plan
- Incremental development by family; each family merges when its charts compile and have an example.
- Publish to PyPI only when all 43 are ported and the gallery is complete (Phase 8 gate).
- Semantic versioning; preserve the MIT license and attribution to rosencharts.

## 10. Open Questions
- [ ] Theming by tokens (palette) in v1 or v2? — Owner: Ernesto
- [ ] Which charts really require `NoSSRComponent`? — confirm in the Phase 1 spike
- [ ] Publish as a Reflex "custom component" (`reflex component`) or a flat package? — Owner: Ernesto

---

## Change History

| Version | Date | Author | Changes |
|---|---|---|---|
| 1.0 | 2026-06-14 | Ernesto Crespo | Initial version |
