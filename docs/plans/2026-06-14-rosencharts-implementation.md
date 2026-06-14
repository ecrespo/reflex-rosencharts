# reflex-rosencharts — Implementation Plan (43 charts + demo gallery)

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Use superpowers:test-driven-development for every wrapper. The 42 non-pilot charts are dispatched via a multi-agent Workflow after the pilot recipe is proven (Stage A gate).

**Goal:** Port all 43 rosencharts D3/TSX charts to Reflex Python components, each with a parametrized TSX, a typed Python wrapper, a TDD test, and an example page in a navigable demo gallery.

**Architecture:** Each chart is wrapped as a local React component via `rx.asset(...)` + `library="$/public{path}"`. Hardcoded data in each TSX becomes a `data` prop (default = original example). Charts using `ClientTooltip` (createPortal) are wrapped as `NoSSRComponent`. Tailwind V4 (already enabled) styles the charts; dynamic classes that arrive via props are safelisted. A demo app renders one example per chart.

**Tech Stack:** Python 3.13, Reflex ≥0.9.5, D3.js (npm), Tailwind V4 (Reflex plugin), React/react-dom, pytest, Playwright (screenshots).

---

## Conventions (apply to every task)

- **TDD cycle per chart:** RED (write failing test) → run/confirm fail → GREEN (TSX + wrapper) → run/confirm pass → REFACTOR → commit.
- **Exact paths:** `reflex_rosencharts/components/<family>/<name>.{py,tsx}`, tests in `tests/test_<family>.py`.
- **Re-export** every public function in `components/<family>/__init__.py` AND `reflex_rosencharts/__init__.py`.
- **Commit** after each chart turns green. Branch first (we are on `master`/`main`).
- Reference: original TSX lives in `reference/rosencharts/<family>-charts/<n>_<Name>.tsx` (read-only).

---

## Stage A — Foundation + pilot (sequential, by the lead; proves the recipe)

### Task A0: Branch + test harness

**Files:**
- Create: `tests/__init__.py`, `tests/conftest.py`, `tests/test_imports.py`
- Modify: `pyproject.toml` (add dev deps: `pytest`, `pytest-cov`)

**Steps:**
1. Create branch: `git checkout -b feat/port-43-charts`.
2. Add dev dependencies: `uv add --dev pytest pytest-cov`.
3. Write `tests/test_imports.py`:
   ```python
   import importlib
   def test_package_imports():
       mod = importlib.import_module("reflex_rosencharts")
       assert hasattr(mod, "__version__")
   ```
4. Run: `uv run pytest tests/test_imports.py -v` → Expected: PASS.
5. Commit: `git commit -am "test: bootstrap pytest harness"`.

### Task A1: Port ClientTooltip helper

**Files:**
- Create: `reflex_rosencharts/components/helpers/ClientTooltip.tsx` (copy of reference, unchanged exports)
- Create: `reflex_rosencharts/components/helpers/client_tooltip.py`
- Test: `tests/test_helpers.py`

**Step 1 (RED):** `tests/test_helpers.py`:
```python
def test_client_tooltip_importable():
    from reflex_rosencharts.components.helpers import client_tooltip as ct
    assert hasattr(ct, "ClientTooltip")
```
**Step 2:** Run `uv run pytest tests/test_helpers.py -v` → Expected: FAIL (ImportError).
**Step 3 (GREEN):**
- Copy `reference/rosencharts/helpers/ClientTooltip.tsx` → `reflex_rosencharts/components/helpers/ClientTooltip.tsx` verbatim.
- `client_tooltip.py`: declare a `NoSSRComponent` for each export (`ClientTooltip`, `TooltipTrigger`, `TooltipContent`) with `library = f"$/public{rx.asset('./ClientTooltip.tsx', shared=True)}"` and matching `tag`. (Helper is composed inside the chart TSX, so the Python wrapper mainly guarantees the asset ships; final shape confirmed during this task.)
- Export `ClientTooltip` in `helpers/__init__.py`.
**Step 4:** Run `uv run pytest tests/test_helpers.py -v` → Expected: PASS.
**Step 5:** Commit `feat: port ClientTooltip helper`.

### Task A2: Tailwind V4 dynamic-class spike

**Files:**
- Modify: `rxconfig.py` (TailwindV4Plugin config — content/safelist)
- Create: `docs/notes/tailwind-safelist.md` (document what was needed)

**Steps:**
1. Confirm `TailwindV4Plugin` scans the TSX under `reflex_rosencharts/components/**`. Add the components glob to the Tailwind `content` if not auto-included.
2. Add a **safelist** for classes that arrive via props / are built dynamically (e.g. `stroke-fuchsia-400`, `text-fuchsia-300`, palette colors). Start minimal; expand as charts need.
3. Validate by building once (Task A4 export) — defer assertion to A4.
4. Commit `chore: configure Tailwind V4 content+safelist for chart classes`.

### Task A3: d3 dependency wiring

**Decision in this task:** D3 is imported inside the TSX (`from "d3"`). The wrapper that owns the TSX must declare `lib_dependencies = ["d3"]` (and `@types/d3` if needed). Confirmed/applied in Task A4 on the pilot wrapper.

### Task A4: Pilot — line_chart (full recipe, TDD)

**Files:**
- Create: `reflex_rosencharts/components/line/line_chart.tsx`
- Create: `reflex_rosencharts/components/line/line_chart.py`
- Modify: `reflex_rosencharts/components/line/__init__.py`, `reflex_rosencharts/__init__.py`
- Test: `tests/test_line.py`

**Step 1 (RED):** `tests/test_line.py`:
```python
def test_line_chart_builds_component():
    import reflex_rosencharts as rxc
    import reflex as rx
    comp = rxc.line_chart(data=[{"date": "2023-05-01", "value": 6}])
    assert isinstance(comp, rx.Component)

def test_line_chart_default_data_matches_example():
    import reflex_rosencharts as rxc
    comp = rxc.line_chart()  # no args → reproduces original example
    assert isinstance(comp.data, (list, object))  # default present
```
**Step 2:** Run `uv run pytest tests/test_line.py -v` → Expected: FAIL (no attribute `line_chart`).
**Step 3 (GREEN):**
- Copy `reference/rosencharts/line-charts/1_LineChart.tsx` → `components/line/line_chart.tsx`.
- Parametrize: replace hardcoded `sales`/`data` with `export function LineChart({ data = <originalSales>, color = "stroke-fuchsia-400" })`; build the `Date`-mapped array from `data` inside the component; fix helper import to `../helpers/ClientTooltip`.
- `line_chart.py`:
  ```python
  import reflex as rx
  from typing import TypedDict

  class LinePoint(TypedDict):
      date: str
      value: float

  _DEFAULT = [{"date": "2023-04-30", "value": 4}, ...]  # original example
  _path = rx.asset("./line_chart.tsx", shared=True)

  class LineChart(rx.NoSSRComponent):  # NoSSR: uses ClientTooltip portal
      library = f"$/public{_path}"
      tag = "LineChart"
      is_default = False
      lib_dependencies = ["d3"]
      data: rx.Var[list[LinePoint]] = rx.Var.create(_DEFAULT)
      color: rx.Var[str] = rx.Var.create("stroke-fuchsia-400")
      on_point_hover: rx.EventHandler[rx.event.passthrough_event_spec(dict)]

  def line_chart(**props) -> rx.Component:
      return LineChart.create(**props)
  ```
- Re-export `line_chart` in both `__init__.py` files.
**Step 4:** Run `uv run pytest tests/test_line.py -v` → Expected: PASS.
**Step 5:** Commit `feat(line): port line_chart pilot end-to-end`.

### Task A5: Demo gallery skeleton + pilot page

**Files:**
- Rewrite: `reflex_rosencharts/reflex_rosencharts.py`
- Create: `reflex_rosencharts/gallery/__init__.py`, `reflex_rosencharts/gallery/registry.py`

**Steps:**
1. Build a `registry.py` mapping family → list of `(name, render_callable, snippet)`. Seed with `line_chart`.
2. Rewrite the demo app: sidebar listing the 8 families; main area renders a card per chart (the chart with default data + a `rx.code_block` snippet).
3. Add `rx.color_mode.button` for dark-mode check.
4. Commit `feat(demo): gallery skeleton with sidebar + pilot card`.

### Task A6: GATE — verify pilot compiles & renders

**Steps:**
1. Run `uv run reflex export --no-zip` (or `reflex run` briefly) → Expected: builds with no TSX/Tailwind errors.
2. Screenshot the pilot page (Playwright, Stage C tooling) and eyeball vs `reference/`.
3. If broken, fix recipe HERE before any fan-out. **Do not proceed to Stage B until this gate passes.**
4. Commit any fixes; tag the proven recipe in `CONTRIBUTING.md` (port recipe section).

---

## Stage B — Fan-out: remaining 42 charts (multi-agent Workflow, by family)

**Precondition:** Stage A gate passed. The proven recipe + the pilot files serve as the template each agent copies.

**Per-chart task template (each agent runs this, TDD):**

```
Inputs: family, name, reference_path, data_schema, uses_tooltip(bool), extra_props
RED   → tests/test_<family>.py::test_<name>_builds_component  (and default-data test)
        run → confirm FAIL
GREEN → 1. copy reference_path → components/<family>/<name>.tsx
         2. parametrize hardcoded data → `data` prop (default = original example)
         3. fix helper import path if uses_tooltip
         4. write components/<family>/<name>.py wrapper:
              - rx.NoSSRComponent if uses_tooltip else rx.Component
              - library=f"$/public{rx.asset('./<name>.tsx', shared=True)}", tag, is_default=False
              - lib_dependencies=["d3"] when the TSX imports d3
              - typed props per API spec (data, color/colors, height, width, class_name, events)
         5. re-export in components/<family>/__init__.py + reflex_rosencharts/__init__.py
         6. register in gallery/registry.py with usage snippet
        run → confirm PASS
REFACTOR → keep green; commit `feat(<family>): port <name>`
```

**Catalog (42 remaining — one task each):**

- **Line (7):** line_chart_curved, line_chart_step, line_chart_pulse, line_chart_labels_curved, line_chart_full, line_chart_stocks_curved, line_chart_multiple (multi-series: `data`+`data2`).
- **Area (4):** area_chart, area_chart_full, area_chart_gradient, area_chart_semi_filled. (schema = TimePoint)
- **Bar (12):** bar_chart_horizontal, bar_chart_horizontal_logo, bar_chart_gradient, bar_chart_breakdown, bar_chart_thin_breakdown, bar_chart_thin_horizontal, bar_chart_flags_horizontal, bar_chart_vertical, bar_chart_multi_vertical, bar_chart_triple_flags_horizontal, bar_chart_line, bar_chart_benchmark. (schema = BarItem + variant extras)
- **Pie/Donut (8):** pie_chart, pie_chart_stocks, pie_chart_labels, donut_chart, donut_chart_center_text, donut_chart_half, donut_chart_fillable_half, donut_chart_fillable. (schema = CategoryValue; `colors` palette; `center_text`/`value` extras)
- **Scatter (4):** scatter_chart, scatter_chart_interactive (on_point_click), scatter_chart_multiclass (class color), scatter_chart_stocks. (schema = ScatterPoint)
- **Treemap (3):** treemap_chart, treemap_chart_images (img per node), treemap_chart_gradient. (schema = TreemapNode, nested)
- **Radar (2):** radar_chart, radar_chart_rounded. (schema = RadarPoint)
- **Other (2):** bubble_chart (ScatterPoint+size), funnel_chart (FunnelStage).

**Workflow shape:** one pipeline per family; stage 1 = port+test the chart (worktree isolation to avoid file conflicts), stage 2 = self-verify the test passes. Families run in parallel. Schemas/extra props per `specs/data-model` and `specs/api`.

---

## Stage C — Integration + verification

### Task C1: Full test suite + coverage
- Run `uv run pytest --cov=reflex_rosencharts --cov-report=term-missing` → Expected: all green, coverage > 70%.
- Fix any re-export gaps in `reflex_rosencharts/__init__.py`.
- Commit.

### Task C2: Gallery complete + compile gate
- Ensure `gallery/registry.py` has all 43; the demo lists every family with cards.
- Run `uv run reflex export --no-zip` → Expected: builds clean (no TSX/Tailwind errors).
- Commit.

### Task C3: Playwright screenshots vs reference
- Use the `playwright` skill. Launch the app; capture each chart page to `docs/screenshots/<name>.png`.
- Eyeball each vs `reference/` (visual-parity audit by family). Note discrepancies for follow-up.
- Commit screenshots + an audit note.

### Task C4: Docs
- Update `README.md` (install, quickstart, gallery of snippets) and `CONTRIBUTING.md` (final port recipe).
- Commit.

---

## Definition of Done

- [ ] 43 wrappers + parametrized TSX, all re-exported from `reflex_rosencharts`.
- [ ] `uv run pytest` green; coverage > 70%.
- [ ] Demo gallery lists all 43; `reflex export` compiles clean.
- [ ] Playwright screenshots captured for all 43; parity audited per family.
