# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.2] - 2026-09-13

### Fixed

- **Scatter charts: x axis labels are now regular ticks.** They used to be data
  points (index 0, every fifth one and the last), which produced irregular
  jumps, labels that overlapped into unreadable pairs on clustered data, and an
  axis that changed whenever the data changed. Labels are now generated from the
  same tick list as the grid lines, so the two always line up, and the number of
  ticks adapts to the measured width of the chart (no overlap at phone widths).
- **Scatter charts: domains come from the extent of the data, not its order.**
  `scatter_chart`, `scatter_chart_interactive` and `scatter_chart_stocks` took
  `data[0]` and `data[data.length - 1]` as the x domain, so unsorted data
  produced a broken axis and tooltip bands with negative widths. Both axes now
  use the minimum and maximum, and the tooltip bands are computed on a sorted
  copy (the `data` prop is never mutated). Shuffling the input now renders the
  same chart.
- **Scatter charts: no point is clipped at the edges.** The mark radius is
  reserved in the scale's *range*, so the dot with the highest x or y value —
  and its larger hover state — stays fully inside the plot area. The domain is
  snapped outwards to whole tick steps in a single pass, so there is always a
  labelled reference at or beyond the extremes without wasting a fifth of the
  axis, as d3's iterative `.nice()` does.
- **Scatter charts: clustered points stay hoverable.** Points sharing an x value
  used to get a zero-width tooltip band and no tooltip at all; the dot itself is
  now a trigger as well.
- **Scatter and line charts: the y-axis gutter fits its labels.** The fixed
  `--marginLeft: 25px` wrapped 3+ digit labels such as `400` or `1000` onto two
  lines, which consumers had to patch with global CSS. The gutter is now derived
  from the longest label.

### Added

- `margin_left` prop on the scatter charts and on `line_chart`,
  `line_chart_curved`, `line_chart_multiple`, `line_chart_pulse`,
  `line_chart_step` and `line_chart_stocks_curved`: overrides the y-axis gutter
  (`"46px"` or `46`). Optional; the computed value is used when it is omitted.
- `x_scale` / `y_scale` props on the scatter charts: `"linear"` (default),
  `"log"` or `"symlog"`, for data with extreme values. `"log"` requires strictly
  positive values and falls back to `"symlog"` when any value is `<= 0`. Log
  axes spanning a decade or more are labelled with powers of ten; narrower log
  axes and symlog use regular steps. Labels that would collide with their
  neighbour are dropped, but both ends of the axis always stay labelled.
- CI: GitHub Actions workflows for linting (ruff), tests (pytest), package
  build (`reflex component build` + `twine check`), the demo's production
  build with the axis regression checks, and security scans (gitleaks, bandit,
  semgrep, pip-audit, dependency review, CodeQL).
- Shared `components/helpers/ChartAxis.tsx` with the scale, tick, margin and
  tooltip-band helpers, registered like `ClientTooltip.tsx`.
- Demo: a *Scatter axes on clustered data* section — 13 repositories by days
  alive vs. commits, with controls to shuffle the input order, add an extreme
  point and switch the x scale, plus the same chart at 390px.

### Compatibility

No breaking changes: every new prop is optional and defaults to the previous
behaviour where it was sane. Charts fed sorted data render as before, except
for the axis labels, which are now regular ticks.

## [0.2.1] - 2026-06-24

### Fixed

- Render the tooltip trigger as a `<div>` for the DIV-based charts.

## [0.2.0] - 2026-06-24

### Added

- The remaining 39 charts (43 in total, across 8 families), all shown in the demo.
- First 4 charts (area / line / bar / pie) wired to `rx.State` in the demo.
- Restructured the project as a Reflex custom component ready for PyPI.

## [0.1.2] - 2026-06-14

### Changed

- Documentation translated to English; packaging metadata for PyPI.

[0.2.2]: https://github.com/ecrespo/reflex-rosencharts/compare/v0.2.1...v0.2.2
[0.2.1]: https://github.com/ecrespo/reflex-rosencharts/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/ecrespo/reflex-rosencharts/compare/v0.1.2...v0.2.0
[0.1.2]: https://github.com/ecrespo/reflex-rosencharts/releases/tag/v0.1.2
