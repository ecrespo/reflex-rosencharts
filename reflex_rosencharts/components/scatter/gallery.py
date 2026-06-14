"""Gallery entries for the scatter family."""

from ...gallery.registry import ChartEntry
from .scatter_chart import scatter_chart
from .scatter_chart_interactive import scatter_chart_interactive
from .scatter_chart_multiclass import scatter_chart_multiclass
from .scatter_chart_stocks import scatter_chart_stocks

GALLERY_ENTRIES: list[ChartEntry] = [
    ChartEntry(
        name="scatter_chart",
        title="Scatter Chart",
        family="scatter",
        render=lambda fn=scatter_chart: fn(),
        snippet=(
            "import reflex_rosencharts as rxc\n\n"
            "rxc.scatter_chart(\n"
            '    data=[{"revenue": 10, "value": 102.8, "company": "Company A"}, ...],\n'
            '    color="text-violet-400",\n'
            ")"
        ),
    ),
    ChartEntry(
        name="scatter_chart_interactive",
        title="Scatter Chart (Interactive)",
        family="scatter",
        render=lambda fn=scatter_chart_interactive: fn(),
        snippet=(
            "import reflex_rosencharts as rxc\n\n"
            "rxc.scatter_chart_interactive(\n"
            '    data=[{"revenue": 10, "value": 102.8, "company": "Company A"}, ...],\n'
            "    on_point_click=State.handle_click,  # receives {revenue, value, company}\n"
            ")"
        ),
    ),
    ChartEntry(
        name="scatter_chart_multiclass",
        title="Scatter Chart (Multiclass)",
        family="scatter",
        render=lambda fn=scatter_chart_multiclass: fn(),
        snippet=(
            "import reflex_rosencharts as rxc\n\n"
            "rxc.scatter_chart_multiclass(\n"
            '    data=[{"revenue": 10, "value": 102.8, "company": "Green A", "class": "green"}, ...],\n'
            '    class_colors={"green": "text-lime-500", "blue": "text-sky-500"},\n'
            ")"
        ),
    ),
    ChartEntry(
        name="scatter_chart_stocks",
        title="Scatter Chart (Stocks / Logos)",
        family="scatter",
        render=lambda fn=scatter_chart_stocks: fn(),
        snippet=(
            "import reflex_rosencharts as rxc\n\n"
            "rxc.scatter_chart_stocks(\n"
            '    data=[{"revenue": 10, "value": 500, "company": "Company A"}, ...],\n'
            ")"
        ),
    ),
]
