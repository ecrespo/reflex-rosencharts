"""Gallery entries for the treemap family."""

from ...gallery.registry import ChartEntry
from .treemap_chart import treemap_chart
from .treemap_chart_gradient import treemap_chart_gradient
from .treemap_chart_images import treemap_chart_images

GALLERY_ENTRIES: list[ChartEntry] = [
    ChartEntry(
        name="treemap_chart",
        title="Treemap Chart",
        family="treemap",
        render=lambda fn=treemap_chart: fn(),
        snippet=(
            "import reflex_rosencharts as rxc\n\n"
            "rxc.treemap_chart(\n"
            '    data=[{"topic": "Tech", "subtopics": [{"Windows": 100, "MacOS": 120}]}],\n'
            ")"
        ),
    ),
    ChartEntry(
        name="treemap_chart_images",
        title="Treemap Chart (Images)",
        family="treemap",
        render=lambda fn=treemap_chart_images: fn(),
        snippet=(
            "import reflex_rosencharts as rxc\n\n"
            "rxc.treemap_chart_images(\n"
            "    data=[{\n"
            '        "topic": "Tech",\n'
            '        "subtopics": [{"name": "Apple", "value": 100, "logo": "https://.../a.svg"}],\n'
            "    }],\n"
            ")"
        ),
    ),
    ChartEntry(
        name="treemap_chart_gradient",
        title="Treemap Chart (Gradient)",
        family="treemap",
        render=lambda fn=treemap_chart_gradient: fn(),
        snippet=(
            "import reflex_rosencharts as rxc\n\n"
            "rxc.treemap_chart_gradient(\n"
            '    data=[{"topic": "Tech", "subtopics": [{"name": "Apple", "value": 100}]}],\n'
            ")"
        ),
    ),
]
