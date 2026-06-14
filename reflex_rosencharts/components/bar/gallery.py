"""Gallery entries for the bar family."""

from ...gallery.registry import ChartEntry
from .bar_chart_benchmark import bar_chart_benchmark
from .bar_chart_breakdown import bar_chart_breakdown
from .bar_chart_flags_horizontal import bar_chart_flags_horizontal
from .bar_chart_gradient import bar_chart_gradient
from .bar_chart_horizontal import bar_chart_horizontal
from .bar_chart_horizontal_logo import bar_chart_horizontal_logo
from .bar_chart_line import bar_chart_line
from .bar_chart_multi_vertical import bar_chart_multi_vertical
from .bar_chart_thin_breakdown import bar_chart_thin_breakdown
from .bar_chart_thin_horizontal import bar_chart_thin_horizontal
from .bar_chart_triple_flags_horizontal import bar_chart_triple_flags_horizontal
from .bar_chart_vertical import bar_chart_vertical

GALLERY_ENTRIES: list[ChartEntry] = [
    ChartEntry(
        name="bar_chart_horizontal",
        title="Bar Chart Horizontal",
        family="bar",
        render=lambda fn=bar_chart_horizontal: fn(),
        snippet=(
            "import reflex_rosencharts as rxc\n\n"
            "rxc.bar_chart_horizontal(\n"
            '    data=[{"key": "Technology", "value": 38.1}, ...],\n'
            ")"
        ),
    ),
    ChartEntry(
        name="bar_chart_horizontal_logo",
        title="Bar Chart Horizontal (Logos)",
        family="bar",
        render=lambda fn=bar_chart_horizontal_logo: fn(),
        snippet=(
            "import reflex_rosencharts as rxc\n\n"
            "rxc.bar_chart_horizontal_logo(\n"
            '    data=[{"key": "Company A", "value": 55.8,\n'
            '           "color": "bg-pink-300 dark:bg-pink-400"}, ...],\n'
            ")"
        ),
    ),
    ChartEntry(
        name="bar_chart_gradient",
        title="Bar Chart Gradient",
        family="bar",
        render=lambda fn=bar_chart_gradient: fn(),
        snippet=(
            "import reflex_rosencharts as rxc\n\n"
            "rxc.bar_chart_gradient(\n"
            '    data=[{"key": "Technology", "value": 38.1,\n'
            '           "color": "from-pink-300 to-pink-400"}, ...],\n'
            ")"
        ),
    ),
    ChartEntry(
        name="bar_chart_breakdown",
        title="Bar Chart Breakdown",
        family="bar",
        render=lambda fn=bar_chart_breakdown: fn(),
        snippet=(
            "import reflex_rosencharts as rxc\n\n"
            "rxc.bar_chart_breakdown(\n"
            '    data=[{"key": "Energy", "value": 27.1,\n'
            '           "color": "from-blue-300 to-blue-400"}, ...],\n'
            ")"
        ),
    ),
    ChartEntry(
        name="bar_chart_thin_breakdown",
        title="Bar Chart Thin Breakdown",
        family="bar",
        render=lambda fn=bar_chart_thin_breakdown: fn(),
        snippet=(
            "import reflex_rosencharts as rxc\n\n"
            "rxc.bar_chart_thin_breakdown(\n"
            '    data=[{"key": "Energy", "value": 27.1,\n'
            '           "color": "from-blue-300 to-blue-400"}, ...],\n'
            ")"
        ),
    ),
    ChartEntry(
        name="bar_chart_thin_horizontal",
        title="Bar Chart Thin Horizontal",
        family="bar",
        render=lambda fn=bar_chart_thin_horizontal: fn(),
        snippet=(
            "import reflex_rosencharts as rxc\n\n"
            "rxc.bar_chart_thin_horizontal(\n"
            '    data=[{"key": "France", "value": 38.1}, ...],\n'
            ")"
        ),
    ),
    ChartEntry(
        name="bar_chart_flags_horizontal",
        title="Bar Chart Flags Horizontal",
        family="bar",
        render=lambda fn=bar_chart_flags_horizontal: fn(),
        snippet=(
            "import reflex_rosencharts as rxc\n\n"
            "rxc.bar_chart_flags_horizontal(\n"
            '    data=[{"key": "Portugal", "value": 55.8, "flag": "pt"}, ...],\n'
            ")"
        ),
    ),
    ChartEntry(
        name="bar_chart_vertical",
        title="Bar Chart Vertical",
        family="bar",
        render=lambda fn=bar_chart_vertical: fn(),
        snippet=(
            "import reflex_rosencharts as rxc\n\n"
            "rxc.bar_chart_vertical(\n"
            '    data=[{"key": "Technology", "value": 18.1}, ...],\n'
            ")"
        ),
    ),
    ChartEntry(
        name="bar_chart_multi_vertical",
        title="Bar Chart Multi Vertical",
        family="bar",
        render=lambda fn=bar_chart_multi_vertical: fn(),
        snippet=(
            "import reflex_rosencharts as rxc\n\n"
            "rxc.bar_chart_multi_vertical(\n"
            '    data=[{"key": "Jan 2020", "values": [11.1, 9.5]}, ...],\n'
            '    colors=["#B89DFB", "#e7deff"],\n'
            ")"
        ),
    ),
    ChartEntry(
        name="bar_chart_triple_flags_horizontal",
        title="Bar Chart Triple Flags Horizontal",
        family="bar",
        render=lambda fn=bar_chart_triple_flags_horizontal: fn(),
        snippet=(
            "import reflex_rosencharts as rxc\n\n"
            "rxc.bar_chart_triple_flags_horizontal(\n"
            '    data=[{"key": "European Union",\n'
            '           "values": [15, 25, 33], "flag": "eu"}, ...],\n'
            ")"
        ),
    ),
    ChartEntry(
        name="bar_chart_line",
        title="Bar Chart + Line",
        family="bar",
        render=lambda fn=bar_chart_line: fn(),
        snippet=(
            "import reflex_rosencharts as rxc\n\n"
            "rxc.bar_chart_line(\n"
            '    data=[{"key": "Jan", "metric1": 18.1, "metric2": 700}, ...],\n'
            ")"
        ),
    ),
    ChartEntry(
        name="bar_chart_benchmark",
        title="Bar Chart Benchmark",
        family="bar",
        render=lambda fn=bar_chart_benchmark: fn(),
        snippet=(
            "import reflex_rosencharts as rxc\n\n"
            "rxc.bar_chart_benchmark(\n"
            '    data=[{"key": "Model 0", "value": 85.8}, ...],\n'
            ")"
        ),
    ),
]
