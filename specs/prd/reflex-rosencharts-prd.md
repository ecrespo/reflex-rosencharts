# reflex-rosencharts

## Product Requirements Document (PRD)

| Field | Value |
|---|---|
| **Author** | Ernesto Crespo |
| **Status** | `DRAFT` |
| **Version** | 1.0 |
| **Date** | 2026-06-14 |
| **Reviewers** | — |
| **Last updated** | 2026-06-14 |

---

## 1. Executive Summary

`reflex-rosencharts` is a **Reflex custom component** that ports the charting library
[rosencharts](https://github.com/Filsommer/rosenCharts) (43 React/TSX components built with
D3.js and Tailwind CSS) to the **Reflex** ecosystem, allowing Python developers to build
dashboards and visualizations without writing JavaScript.

It targets Python developers using Reflex who need modern, lightweight, and
aesthetic charts. It solves the problem that rosencharts today is only consumable as a "copy-paste" of
TSX inside React/Next.js projects; this port exposes each chart as a Python function
(`rxc.line_chart(...)`, `rxc.donut_chart(...)`, etc.) with typed props and data passed from the
application state.

## 2. Context and Problem

### 2.1 Current Situation
- rosencharts is a collection of 43 `.tsx` components (it is not an npm package) that the user
  copies and pastes into their React project, installing `d3` and `@types/d3` manually.
- Each component ships with **hardcoded data** and **Tailwind** classes for styling.
- 29 of the 43 charts depend on a local helper `ClientTooltip.tsx` (using `react-dom` / `createPortal`).
- There is no way to use these charts from Python/Reflex.

### 2.2 Problem
Reflex developers do not have access to these charts. Reflex's native options
(recharts, plotly) have a different aesthetic. Rewriting 43 D3 charts by hand in each project
is costly and error-prone.

### 2.3 Opportunity
Reflex supports **wrapping local React components** (`rx.asset` + `library="$/public..."`).
By packaging the rosencharts TSX files as local components and exposing them as
`rx.Component` classes, you get a reusable library, installable via `pip`/`uv`, that covers the 8
chart families with a single coherent Python API.

## 3. Target Users

### Persona 1: Python / Reflex Developer
- **Description:** Builds data-driven web applications in Python with Reflex.
- **Main need:** Insert attractive charts by passing data from `rx.State`.
- **Usage frequency:** Daily during dashboard development.
- **Technical level:** Medium/High in Python, low/none in React/D3.

### Persona 2: Data Scientist / Analyst
- **Description:** Creates visualization prototypes and internal reports.
- **Main need:** Ready-to-use charts with little configuration.
- **Usage frequency:** Weekly.
- **Technical level:** Medium in Python, low in frontend.

### Persona 3: Library Contributor
- **Description:** Maintains/extends the port.
- **Main need:** A clear and repeatable pattern for porting each chart.
- **Usage frequency:** Occasional.
- **Technical level:** High in Python and React.

## 4. Goals and Success Metrics

### 4.1 Project Goals

| Goal | Metric | Target | Timeframe |
|---|---|---|---|
| Chart coverage | % of the 43 charts ported | 100% | End of Phase 7 |
| Usage examples | Each chart with a runnable example in the demo app | 43/43 | End of Phase 7 |
| Visual parity | Acceptable visual difference vs. original (review by screenshot) | ≥ 95% similar | Per chart |
| Publication | Installable package (`pip install reflex-rosencharts`) | Published on PyPI | Phase 8 |

### 4.2 User Goals

| User Goal | Indicator |
|---|---|
| Insert a chart in < 5 lines of Python | Snippet in README per chart |
| Pass data from state without touching JS | All charts accept `data` as a prop |
| Consistent theming (light/dark) | Dark mode support via Tailwind |

## 5. Scope

### 5.1 In Scope (Included)
- [ ] Port of the **43 charts** across 8 families: area (4), bar (12), line (8), pie/donut (8), scatter (4), treemap (3), radar (2), other (2).
- [ ] Parameterization of **data** (replace the hardcoded data with props fed from Python).
- [ ] Port of the `ClientTooltip` helper (required by 29 charts).
- [ ] Integration of **Tailwind CSS** into the Reflex build.
- [ ] A **demo app** (`reflex_rosencharts/reflex_rosencharts.py`) with one example page per chart (the "examples folder").
- [ ] Documentation: README + docstrings + gallery page.
- [ ] Packaging as a publishable Reflex custom component.

### 5.2 Out of Scope (Excluded)
- Creating new charts that do not exist in rosencharts — only the existing ones are ported.
- Data backends, authentication, or persistence — the library only renders.
- Animations/interactions not present in the original.
- Versioning/patching D3 beyond what is necessary to render.

### 5.3 Future Considerations
- Export charts to PNG/SVG.
- Token-based theming (configurable palettes) instead of fixed Tailwind classes.
- Support for streaming/real-time data updates.

## 6. Functional Requirements

### RF-001: Render each chart as a Reflex component
- **Description:** The system must expose each of the 43 charts as a Python function that returns an `rx.Component`.
- **Actor:** Python developer.
- **Preconditions:** `reflex-rosencharts` installed; Tailwind enabled.
- **Main flow:**
  1. The developer imports `reflex_rosencharts as rxc`.
  2. Calls `rxc.<chart>(data=...)` inside a Reflex page.
  3. Reflex compiles the local TSX and renders the chart.
- **Postconditions:** The chart is displayed with the provided data.
- **Priority:** `MUST`

### RF-002: Feed data from state
- **Description:** Each chart must accept its dataset via the `data` prop (and specific props) typed with `rx.Var`.
- **Actor:** Python developer.
- **Main flow:** The data lives in `rx.State`; when it changes, the chart re-renders.
- **Priority:** `MUST`

### RF-003: Interactive tooltips
- **Description:** Charts that use `ClientTooltip` in the original must show the same tooltip on hover.
- **Preconditions:** `ClientTooltip` helper ported and available.
- **Priority:** `SHOULD`

### RF-004: Runnable example per chart
- **Description:** The system must include one example page per chart in the demo app, replicating the "example" from the original repo.
- **Priority:** `MUST`

### RF-005: Dark mode support
- **Description:** Charts must respect Tailwind's `dark:` variants as in the original.
- **Priority:** `SHOULD`

### RF-006: Style/size props
- **Description:** Each chart must allow adjusting dimensions and, where applicable, colors/palette.
- **Priority:** `COULD`

## 7. Non-Functional Requirements

### Performance
- Reflex's incremental compilation time must not degrade noticeably; the charts are lightweight components (D3 on the client).
- The initial render of a page with a chart must be < 1s locally.

### Maintainability
- A **repeatable and documented** port pattern (one recipe per chart type).
- Test coverage > 70% of the Python wrapper code.
- Each wrapper in its own module within the corresponding family.

### Compatibility
- Python ≥ 3.10 (project pinned to 3.13).
- Reflex ≥ 0.9.x.
- Evergreen browsers (Chrome, Firefox, Safari, Edge).

### Observability
- TSX compilation errors must be visible in the Reflex console.

## 8. Constraints and Dependencies

### Technical Constraints
- rosencharts **is not an npm package**: the TSX files must be treated as **local components** (`rx.asset`).
- The charts use **Tailwind**: this requires enabling Reflex's Tailwind plugin.
- `ClientTooltip` uses `react-dom`/`createPortal`: candidates for `NoSSRComponent` where necessary.
- Hardcoded data in each TSX → refactor to receive `props`.

### Business / License Constraints
- rosencharts is **MIT**: the port must preserve the MIT attribution and license.

### External Dependencies

| Dependency | Type | Owner | Status | Risk |
|---|---|---|---|---|
| Reflex (framework) | Runtime | reflex-dev | Stable | Low |
| D3.js | Runtime (npm) | d3 | Stable | Low |
| Tailwind CSS | Build | tailwindlabs | Stable | Medium (config in Reflex) |
| rosencharts (TSX source code) | Source | Filsommer | Stable | Low |
| react-dom (tooltip portals) | Runtime | Meta | Stable | Low |

## 9. User Stories

### Epic: Chart gallery in Python

**US-001:** As a Reflex developer, I want to call `rxc.line_chart(data=my_series)`, to display a line without writing JS.
- Acceptance criteria:
  - [ ] The function exists and accepts typed `data`.
  - [ ] The chart renders the same as the original example.

**US-002:** As an analyst, I want a gallery with all the examples, to choose the right chart.
- Acceptance criteria:
  - [ ] The demo app lists the 43 charts with their example.

**US-003:** As a contributor, I want a port guide per type, to add charts following a pattern.
- Acceptance criteria:
  - [ ] The Tech Design documents the wrapping recipe.

## 10. Wireframes / Mockups
- Gallery: sidebar with families (Area, Bar, Line, Pie, Scatter, Treemap, Radar, Other) and, for each one, cards with the chart + code snippet. Visual reference: the `reference/rosencharts/*` files.

## 11. Risks and Mitigations

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| Complex Tailwind configuration in Reflex | Medium | High | Initial spike in Phase 1; document config |
| Portal-based tooltips not compatible with SSR | Medium | Medium | Use `NoSSRComponent` / dynamic import |
| Data refactor breaks the aesthetic | Medium | Medium | Screenshot comparison against original |
| Reflex version changes in its wrapping API | Low | Medium | Pin the Reflex version in pyproject |

## 12. Estimated Timeline

| Phase | Estimated Duration | Deliverable |
|---|---|---|
| Spec & Design | 0.5 week | Approved specs |
| Foundation (Tailwind + helper + pattern) | 1 week | 1st chart working |
| Port by families | 3-4 weeks | 43 charts + examples |
| Demo/gallery + docs | 1 week | Navigable gallery |
| Packaging and publication | 0.5 week | Package on PyPI |

---

## Change History

| Version | Date | Author | Changes |
|---|---|---|---|
| 1.0 | 2026-06-14 | Ernesto Crespo | Initial version |

## Approvals

| Role | Name | Date | Status |
|---|---|---|---|
| Owner | Ernesto Crespo | | ☐ Pending |
| Tech Lead | | | ☐ Pending |
