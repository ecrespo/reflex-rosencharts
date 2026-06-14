# Visual parity audit — 43/43

Screenshots taken from the demo gallery (`reflex run`) with Playwright + system Chrome
(`scripts/screenshot_gallery.py`), default data = original example of each chart.

- **`_gallery_full.png`** — full gallery (sidebar + 43 cards).
- **`<name>.png`** — one per chart (43 files).

## Result

- **43/43 charts render** with the rosencharts aesthetic (D3 + Tailwind), with no blank cards.
- Representative review by family (different render techniques): `line_chart` (SVG+D3),
  `bar_chart_horizontal` (DIV), `bar_chart_flags_horizontal` (flags), `donut_chart_center_text`
  (SVG + center text), `treemap_chart` (nested DIV), `radar_chart` (polygon), `scatter_chart`.
  All match the original.
- `reflex export` compiles all 43 TSX files together (exit 0).
- 83 pytest tests green; 89% coverage of the Python wrappers.

## Known limitations

- **`bar_chart_horizontal_logo`**: the logos are inline SVGs from the original (not data-driven). They are
  preserved verbatim and assigned by row index; `data` controls keys/values/colors but not
  the logo images. Documented in the wrapper docstring.

## How to regenerate

```bash
uv run reflex run                                   # in one terminal
PYTHONPATH=. .venv/bin/python scripts/screenshot_gallery.py   # in another
```
