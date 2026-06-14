"""Gallery entries for the other family."""

from ...gallery.registry import ChartEntry
from .bubble_chart import bubble_chart
from .funnel_chart import funnel_chart

GALLERY_ENTRIES: list[ChartEntry] = [
    ChartEntry(
        name="bubble_chart",
        title="Bubble Chart",
        family="other",
        render=lambda fn=bubble_chart: fn(),
        snippet=(
            "import reflex_rosencharts as rxc\n\n"
            "rxc.bubble_chart(\n"
            '    data=[{"name": "MacOS", "sector": "Tech", "value": 4812}, ...],\n'
            '    colors=["text-pink-400", "text-violet-500", ...],\n'
            ")"
        ),
    ),
    ChartEntry(
        name="funnel_chart",
        title="Funnel Chart",
        family="other",
        render=lambda fn=funnel_chart: fn(),
        snippet=(
            "import reflex_rosencharts as rxc\n\n"
            "rxc.funnel_chart(\n"
            '    data=[{"name": "Gross Revenue", "value": 47.1}, ...],\n'
            ")"
        ),
    ),
]
