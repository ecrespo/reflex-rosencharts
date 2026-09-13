# reflex-rosencharts

A port of the [**rosencharts**](https://github.com/Filsommer/rosenCharts) charting library
(43 React/TSX components built with D3.js + Tailwind) to a **custom component for
[Reflex](https://reflex.dev/)**, so the charts can be used from pure Python.

> Status: **scaffold + SDD plan**. The charts are implemented in phases according to
> [`specs/plans/implementation-plan.md`](specs/plans/implementation-plan.md).

## Why?

rosencharts is not an npm package: it's a set of `.tsx` components to copy and paste, with
hardcoded data and Tailwind styling. This project wraps them as **local Reflex components**
(`rx.asset` + `library="$/public..."`), parametrizes them to receive data from `rx.State`, and
exposes them as Python functions:

```python
import reflex as rx
import reflex_rosencharts as rxc

class State(rx.State):
    sales: list[dict] = [{"date": "2023-05-01", "value": 6}, {"date": "2023-05-02", "value": 8}]

def index() -> rx.Component:
    return rxc.line_chart(data=State.sales)
```

## Charts (43 across 8 families)

| Family | # | Examples |
|---|---|---|
| Area | 4 | `area_chart`, `area_chart_gradient` |
| Bar | 12 | `bar_chart_horizontal`, `bar_chart_benchmark` |
| Line | 8 | `line_chart`, `line_chart_multiple` |
| Pie/Donut | 8 | `pie_chart`, `donut_chart_center_text` |
| Scatter | 4 | `scatter_chart`, `scatter_chart_interactive` |
| Treemap | 3 | `treemap_chart`, `treemap_chart_images` |
| Radar | 2 | `radar_chart`, `radar_chart_rounded` |
| Other | 2 | `bubble_chart`, `funnel_chart` |

Full catalog and props: [`specs/api/component-api-v1.md`](specs/api/component-api-v1.md).

## Axis options (scatter and line charts)

The scatter charts build both axes from the *extent* of the data, label them with
regular ticks that line up with the grid lines, and reserve room for the dots so
none is clipped at the edges — the data does not have to arrive sorted:

```python
rxc.scatter_chart(
    data=State.repos,      # [{"revenue": x, "value": y, "company": label}, ...]
    x_scale="log",         # "linear" (default), "log" or "symlog"
    margin_left="46px",    # optional; by default it fits the longest y label
)
```

| Prop | Charts | Default |
|---|---|---|
| `margin_left` | the 4 scatter charts, `line_chart`, `line_chart_curved`, `line_chart_multiple`, `line_chart_pulse`, `line_chart_step`, `line_chart_stocks_curved` | computed from the longest y label |
| `x_scale` / `y_scale` | the 4 scatter charts | `"linear"` |

`"log"` needs strictly positive values and falls back to `"symlog"` when any
value is `<= 0`. See [`CHANGELOG.md`](CHANGELOG.md) for what changed in 0.2.2.

## Installation

```bash
pip install reflex-rosencharts
# or, with uv:
uv add reflex-rosencharts
```

## Project layout

This repo is a [Reflex custom component](https://reflex.dev/docs/custom-components/overview/):

```
custom_components/
└── reflex_rosencharts/          # the published package (import name: reflex_rosencharts)
    ├── __init__.py              # public API surface
    ├── reflex_rosencharts.py    # shared base wrapper (RosenChart)
    └── components/<family>/     # chart wrappers, ported in phases
reflex_rosencharts_demo/         # demo app (reflex run) showcasing the component
pyproject.toml                   # packaging metadata (where = ["custom_components"])
```

## Development

Managed with [uv](https://docs.astral.sh/uv/):

```bash
uv sync --extra dev --group test   # install runtime + publishing + test tooling
uv run reflex run                  # start the demo app / gallery
```

Axis regression check for the scatter and line charts (server-renders them with
clustered, unsorted and extreme-valued data and asserts the tick, margin and
clipping guarantees). It uses the frontend dependencies Reflex installs on the
first `reflex run`:

```bash
node scripts/check_scatter_axes.mjs
```

### Build & publish (custom component)

```bash
# 1. Build the sdist + wheel into dist/ (PYTHONPATH=. lets the .pyi step resolve
#    the package under custom_components/).
PYTHONPATH=. uv run reflex component build

# 2. Sanity-check the artifacts.
uv run twine check dist/*

# 3. Publish to PyPI with uv (needs a PyPI API token):
uv publish --token "$PYPI_TOKEN"
# …or to TestPyPI first:
uv publish --publish-url https://test.pypi.org/legacy/ --token "$TEST_PYPI_TOKEN"
```

See Reflex's [command reference](https://reflex.dev/docs/custom-components/command-reference/)
and [publishing prerequisites](https://reflex.dev/docs/custom-components/prerequisites-for-publishing/).

## Specifications (SDD)

The project follows **Spec-Driven Design**. The specs are the primary artifact:

- [PRD](specs/prd/reflex-rosencharts-prd.md) — the what and the who-for
- [API Spec](specs/api/component-api-v1.md) — public Python API (functions, props)
- [Technical Design](specs/technical/architecture.md) — wrapping pattern and architecture
- [Data Model](specs/data-model/chart-data-schemas.md) — per-chart data schemas
- [Implementation Plan](specs/plans/implementation-plan.md) — phases by family

The original code (reference, read-only) lives in [`reference/rosencharts/`](reference/rosencharts/).

## License and attribution

MIT. This project is a port of [rosencharts](https://github.com/Filsommer/rosenCharts)
by Filsommer (MIT). See [`LICENSE`](LICENSE) and [`NOTICE`](NOTICE).
