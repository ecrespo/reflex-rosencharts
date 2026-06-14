# reflex-rosencharts

Port of the charting library [**rosencharts**](https://github.com/Filsommer/rosenCharts)
(43 React/TSX components with D3.js + Tailwind) to a **custom component for
[Reflex](https://reflex.dev/)**, so the charts can be used from pure Python.

> Status: **43/43 charts implemented** ✅ — all with a Python wrapper, parameterized TSX,
> a gallery example, and tests. The demo app (`reflex run`) shows all 43 with their usage snippet.
> Screenshots in [`docs/screenshots/`](docs/screenshots/).

## Why?

rosencharts is not an npm package: it is a set of `.tsx` components meant to be copied and pasted, with
hardcoded data and Tailwind styling. This project wraps them as **local Reflex components**
(`rx.asset` + `library="$/public..."`), parameterizes them to receive data from `rx.State`, and
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

| Family | No. | Examples |
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

## Development

Managed with [uv](https://docs.astral.sh/uv/):

```bash
uv sync                 # install dependencies
uv run reflex run       # start the demo app / gallery (all 43 charts)
uv run pytest           # wrapper tests (TDD)
```

The **demo gallery** lives in `reflex_rosencharts/reflex_rosencharts.py`: a sidebar per family
and one card per chart (chart rendered with sample data + Python snippet). It is the visual test
bench for the port.

## Specifications (SDD)

The project follows **Spec-Driven Design**. The specs are the primary artifact:

- [PRD](specs/prd/reflex-rosencharts-prd.md) — the what and the who
- [API Spec](specs/api/component-api-v1.md) — public Python API (functions, props)
- [Technical Design](specs/technical/architecture.md) — wrapping pattern and architecture
- [Data Model](specs/data-model/chart-data-schemas.md) — data schemas per chart
- [Implementation Plan](specs/plans/implementation-plan.md) — phases per family

The original code (reference, read-only) is in [`reference/rosencharts/`](reference/rosencharts/).

## License and attribution

MIT. This project is a port of [rosencharts](https://github.com/Filsommer/rosenCharts)
by Filsommer (MIT). See [`LICENSE`](LICENSE) and [`NOTICE`](NOTICE).
