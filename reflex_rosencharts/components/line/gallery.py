"""Gallery entries for the line family."""

from ...gallery.registry import ChartEntry
from .line_chart import line_chart

GALLERY_ENTRIES: list[ChartEntry] = [
    ChartEntry(
        name="line_chart",
        title="Line Chart",
        family="line",
        render=lambda: line_chart(),
        snippet=(
            "import reflex_rosencharts as rxc\n\n"
            "rxc.line_chart(\n"
            '    data=[{"date": "2023-05-01", "value": 6}, ...],\n'
            '    color="stroke-fuchsia-400",\n'
            ")"
        ),
    ),
]
