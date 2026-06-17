"""Gallery entries for the radar family."""

from ...gallery.registry import ChartEntry
from .radar_chart import radar_chart
from .radar_chart_rounded import radar_chart_rounded

GALLERY_ENTRIES: list[ChartEntry] = [
    ChartEntry(
        name="radar_chart",
        title="Radar Chart",
        family="radar",
        render=lambda fn=radar_chart: fn(),
        snippet=(
            "import reflex_rosencharts as rxc\n\n"
            "rxc.radar_chart(\n"
            '    data=[{"topic": "Tech", "value": 330}, ...],\n'
            ")"
        ),
    ),
    ChartEntry(
        name="radar_chart_rounded",
        title="Radar Chart Rounded",
        family="radar",
        render=lambda fn=radar_chart_rounded: fn(),
        snippet=(
            "import reflex_rosencharts as rxc\n\n"
            "rxc.radar_chart_rounded(\n"
            '    data=[{"topic": "Tech", "value": 320}, ...],\n'
            ")"
        ),
    ),
]
