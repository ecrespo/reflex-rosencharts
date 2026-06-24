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
