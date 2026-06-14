"""Gallery entries for the area family."""

from ...gallery.registry import ChartEntry
from .area_chart import area_chart
from .area_chart_full import area_chart_full
from .area_chart_gradient import area_chart_gradient
from .area_chart_semi_filled import area_chart_semi_filled

GALLERY_ENTRIES: list[ChartEntry] = [
    ChartEntry(
        name="area_chart",
        title="Area Chart",
        family="area",
        render=lambda fn=area_chart: fn(),
        snippet=(
            "import reflex_rosencharts as rxc\n\n"
            "rxc.area_chart(\n"
            '    data=[{"date": "2023-05-01", "value": 6}, ...],\n'
            '    color="text-purple-200 dark:text-purple-400",\n'
            ")"
        ),
    ),
    ChartEntry(
        name="area_chart_full",
        title="Area Chart Full",
        family="area",
        render=lambda fn=area_chart_full: fn(),
        snippet=(
            "import reflex_rosencharts as rxc\n\n"
            "rxc.area_chart_full(\n"
            '    data=[{"date": "2023-05-01", "value": 6}, ...],\n'
            '    color="text-blue-200 dark:text-blue-400",\n'
            ")"
        ),
    ),
    ChartEntry(
        name="area_chart_gradient",
        title="Area Chart Gradient",
        family="area",
        render=lambda fn=area_chart_gradient: fn(),
        snippet=(
            "import reflex_rosencharts as rxc\n\n"
            "rxc.area_chart_gradient(\n"
            '    data=[{"date": "2023-05-01", "value": 6}, ...],\n'
            '    color_from="text-lime-500 dark:text-lime-100",\n'
            '    color_to="text-lime-50/10 dark:text-green-900",\n'
            ")"
        ),
    ),
    ChartEntry(
        name="area_chart_semi_filled",
        title="Area Chart Semi Filled",
        family="area",
        render=lambda fn=area_chart_semi_filled: fn(),
        snippet=(
            "import reflex_rosencharts as rxc\n\n"
            "rxc.area_chart_semi_filled(\n"
            '    data=[{"date": "2023-05-01", "value": 6}, ...],\n'
            '    color="text-yellow-400 dark:text-yellow-600",\n'
            ")"
        ),
    ),
]
