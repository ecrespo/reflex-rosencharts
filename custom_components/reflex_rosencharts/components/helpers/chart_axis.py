"""Registers the shared ``ChartAxis.tsx`` helper as a frontend asset.

Same mechanism as :mod:`client_tooltip`: the chart TSX files import the axis
helpers through the absolute ``$/public/...`` alias that Reflex generates (see
``CHART_AXIS_IMPORT``), and importing this module from a chart wrapper is what
symlinks the helper into ``assets/external/`` so it ends up in the compiled
frontend.
"""

import reflex as rx

# Symlinked to assets/external/reflex_rosencharts/components/helpers/chart_axis/ChartAxis.tsx
_path = rx.asset("./ChartAxis.tsx", shared=True)

# Build-time module reference used inside the chart .tsx import statements.
CHART_AXIS_IMPORT = f"$/public{_path}"
