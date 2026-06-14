# Auditoría de paridad visual — 43/43

Capturas tomadas de la galería demo (`reflex run`) con Playwright + Chrome del sistema
(`scripts/screenshot_gallery.py`), datos por defecto = ejemplo original de cada gráfica.

- **`_gallery_full.png`** — galería completa (sidebar + 43 tarjetas).
- **`<name>.png`** — una por gráfica (43 archivos).

## Resultado

- **43/43 gráficas renderizan** con la estética de rosencharts (D3 + Tailwind), sin tarjetas en blanco.
- Revisión representativa por familia (técnicas de render distintas): `line_chart` (SVG+D3),
  `bar_chart_horizontal` (DIV), `bar_chart_flags_horizontal` (banderas), `donut_chart_center_text`
  (SVG + texto central), `treemap_chart` (DIV anidado), `radar_chart` (polígono), `scatter_chart`.
  Todas coinciden con el original.
- `reflex export` compila los 43 TSX juntos (exit 0).
- 83 tests pytest verdes; cobertura 89% de los wrappers Python.

## Limitaciones conocidas

- **`bar_chart_horizontal_logo`**: los logos son SVGs inline del original (no data-driven). Se
  preservan verbatim y se asignan por índice de fila; `data` controla keys/values/colores pero no
  las imágenes de logo. Documentado en el docstring del wrapper.

## Cómo regenerar

```bash
uv run reflex run                                   # en una terminal
PYTHONPATH=. .venv/bin/python scripts/screenshot_gallery.py   # en otra
```
