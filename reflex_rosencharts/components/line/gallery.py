"""Gallery entries for the line family."""

from ...gallery.registry import ChartEntry
from .line_chart import line_chart
from .line_chart_curved import line_chart_curved
from .line_chart_full import line_chart_full
from .line_chart_labels_curved import line_chart_labels_curved
from .line_chart_multiple import line_chart_multiple
from .line_chart_pulse import line_chart_pulse
from .line_chart_step import line_chart_step
from .line_chart_stocks_curved import line_chart_stocks_curved

GALLERY_ENTRIES: list[ChartEntry] = [
    ChartEntry(
        name="line_chart",
        title="Line Chart",
        family="line",
        render=lambda fn=line_chart: fn(),
        snippet=(
            "import reflex_rosencharts as rxc\n\n"
            "rxc.line_chart(\n"
            '    data=[{"date": "2023-05-01", "value": 6}, ...],\n'
            '    color="stroke-fuchsia-400",\n'
            ")"
        ),
    ),
    ChartEntry(
        name="line_chart_curved",
        title="Line Chart Curved",
        family="line",
        render=lambda fn=line_chart_curved: fn(),
        snippet=(
            "import reflex_rosencharts as rxc\n\n"
            "rxc.line_chart_curved(\n"
            '    data=[{"date": "2023-05-01", "value": 6}, ...],\n'
            '    color="stroke-violet-400",\n'
            ")"
        ),
    ),
    ChartEntry(
        name="line_chart_multiple",
        title="Line Chart Multiple",
        family="line",
        render=lambda fn=line_chart_multiple: fn(),
        snippet=(
            "import reflex_rosencharts as rxc\n\n"
            "rxc.line_chart_multiple(\n"
            '    data=[{"date": "2023-05-01", "value": 6}, ...],\n'
            '    data2=[{"date": "2023-05-01", "value": 3.5}, ...],\n'
            ")"
        ),
    ),
    ChartEntry(
        name="line_chart_labels_curved",
        title="Line Chart Labels Curved",
        family="line",
        render=lambda fn=line_chart_labels_curved: fn(),
        snippet=(
            "import reflex_rosencharts as rxc\n\n"
            "rxc.line_chart_labels_curved(\n"
            '    data=[{"date": "2023-05-01", "value": 6}, ...],\n'
            ")"
        ),
    ),
    ChartEntry(
        name="line_chart_stocks_curved",
        title="Line Chart Stocks Curved",
        family="line",
        render=lambda fn=line_chart_stocks_curved: fn(),
        snippet=(
            "import reflex_rosencharts as rxc\n\n"
            "rxc.line_chart_stocks_curved(\n"
            '    data=[{"date": "2023-05-01", "value": 6}, ...],\n'
            ")"
        ),
    ),
    ChartEntry(
        name="line_chart_step",
        title="Line Chart Step",
        family="line",
        render=lambda fn=line_chart_step: fn(),
        snippet=(
            "import reflex_rosencharts as rxc\n\n"
            "rxc.line_chart_step(\n"
            '    data=[{"date": "2023-05-01", "value": 6}, ...],\n'
            ")"
        ),
    ),
    ChartEntry(
        name="line_chart_pulse",
        title="Line Chart Pulse",
        family="line",
        render=lambda fn=line_chart_pulse: fn(),
        snippet=(
            "import reflex_rosencharts as rxc\n\n"
            "rxc.line_chart_pulse(\n"
            '    data=[{"date": "2023-05-01", "value": 6}, ...],\n'
            ")"
        ),
    ),
    ChartEntry(
        name="line_chart_full",
        title="Line Chart Full",
        family="line",
        render=lambda fn=line_chart_full: fn(),
        snippet=(
            "import reflex_rosencharts as rxc\n\n"
            "rxc.line_chart_full(\n"
            '    data=[{"date": "2023-05-01", "value": 7}, ...],\n'
            ")"
        ),
    ),
]
