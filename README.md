# reflex-rosencharts

Port de la librería de gráficas [**rosencharts**](https://github.com/Filsommer/rosenCharts)
(43 componentes React/TSX con D3.js + Tailwind) a un **custom component de
[Reflex](https://reflex.dev/)**, para usar las gráficas desde Python puro.

> Estado: **43/43 gráficas implementadas** ✅ — todas con wrapper Python, TSX parametrizado,
> ejemplo en la galería y tests. La app demo (`reflex run`) muestra las 43 con su snippet de uso.
> Capturas en [`docs/screenshots/`](docs/screenshots/).

## ¿Por qué?

rosencharts no es un paquete npm: son componentes `.tsx` para copiar y pegar, con datos
hardcodeados y estilo Tailwind. Este proyecto los envuelve como **componentes locales de Reflex**
(`rx.asset` + `library="$/public..."`), los parametriza para recibir datos desde `rx.State`, y los
expone como funciones Python:

```python
import reflex as rx
import reflex_rosencharts as rxc

class State(rx.State):
    sales: list[dict] = [{"date": "2023-05-01", "value": 6}, {"date": "2023-05-02", "value": 8}]

def index() -> rx.Component:
    return rxc.line_chart(data=State.sales)
```

## Gráficas (43 en 8 familias)

| Familia | Nº | Ejemplos |
|---|---|---|
| Area | 4 | `area_chart`, `area_chart_gradient` |
| Bar | 12 | `bar_chart_horizontal`, `bar_chart_benchmark` |
| Line | 8 | `line_chart`, `line_chart_multiple` |
| Pie/Donut | 8 | `pie_chart`, `donut_chart_center_text` |
| Scatter | 4 | `scatter_chart`, `scatter_chart_interactive` |
| Treemap | 3 | `treemap_chart`, `treemap_chart_images` |
| Radar | 2 | `radar_chart`, `radar_chart_rounded` |
| Other | 2 | `bubble_chart`, `funnel_chart` |

Catálogo completo y props: [`specs/api/component-api-v1.md`](specs/api/component-api-v1.md).

## Desarrollo

Gestionado con [uv](https://docs.astral.sh/uv/):

```bash
uv sync                 # instalar dependencias
uv run reflex run       # arrancar la demo app / galería (las 43 gráficas)
uv run pytest           # tests de los wrappers (TDD)
```

La **galería demo** vive en `reflex_rosencharts/reflex_rosencharts.py`: barra lateral por familia
y una tarjeta por gráfica (gráfica renderizada con datos de ejemplo + snippet Python). Es el banco
de pruebas visual del port.

## Especificaciones (SDD)

El proyecto sigue **Spec-Driven Design**. Las specs son el artefacto primario:

- [PRD](specs/prd/reflex-rosencharts-prd.md) — el qué y el para quién
- [API Spec](specs/api/component-api-v1.md) — API pública Python (funciones, props)
- [Technical Design](specs/technical/architecture.md) — patrón de wrapping y arquitectura
- [Data Model](specs/data-model/chart-data-schemas.md) — esquemas de datos por gráfica
- [Implementation Plan](specs/plans/implementation-plan.md) — fases por familia

El código original (referencia, solo lectura) está en [`reference/rosencharts/`](reference/rosencharts/).

## Licencia y atribución

MIT. Este proyecto es un port de [rosencharts](https://github.com/Filsommer/rosenCharts)
de Filsommer (MIT). Ver [`LICENSE`](LICENSE) y [`NOTICE`](NOTICE).
