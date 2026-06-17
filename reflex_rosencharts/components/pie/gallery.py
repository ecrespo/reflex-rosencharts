"""Gallery entries for the pie / donut family."""

from ...gallery.registry import ChartEntry
from .donut_chart import donut_chart
from .donut_chart_center_text import donut_chart_center_text
from .donut_chart_fillable import donut_chart_fillable
from .donut_chart_fillable_half import donut_chart_fillable_half
from .donut_chart_half import donut_chart_half
from .pie_chart import pie_chart
from .pie_chart_labels import pie_chart_labels
from .pie_chart_stocks import pie_chart_stocks

GALLERY_ENTRIES: list[ChartEntry] = [
    ChartEntry(
        name="pie_chart",
        title="Pie Chart",
        family="pie",
        render=lambda fn=pie_chart: fn(),
        snippet=(
            "import reflex_rosencharts as rxc\n\n"
            "rxc.pie_chart(\n"
            '    data=[{"name": "Rent", "value": 731}, ...],\n'
            '    colors=["#F5A5DB", "#B89DFB", "#758bcf"],\n'
            ")"
        ),
    ),
    ChartEntry(
        name="pie_chart_stocks",
        title="Pie Chart Stocks",
        family="pie",
        render=lambda fn=pie_chart_stocks: fn(),
        snippet=(
            "import reflex_rosencharts as rxc\n\n"
            "rxc.pie_chart_stocks(\n"
            '    data=[{"name": "Apple", "value": 731,\n'
            '           "logo": "https://.../apple.svg",\n'
            '           "color": "text-pink-400"}, ...],\n'
            ")"
        ),
    ),
    ChartEntry(
        name="pie_chart_labels",
        title="Pie Chart Labels",
        family="pie",
        render=lambda fn=pie_chart_labels: fn(),
        snippet=(
            "import reflex_rosencharts as rxc\n\n"
            "rxc.pie_chart_labels(\n"
            '    data=[{"name": "Technology", "value": 731,\n'
            '           "colorFrom": "text-pink-400",\n'
            '           "colorTo": "text-pink-400"}, ...],\n'
            ")"
        ),
    ),
    ChartEntry(
        name="donut_chart",
        title="Donut Chart",
        family="pie",
        render=lambda fn=donut_chart: fn(),
        snippet=(
            "import reflex_rosencharts as rxc\n\n"
            "rxc.donut_chart(\n"
            '    data=[{"name": "AAPL", "value": 30}, ...],\n'
            '    colors=["#7e4cfe", "#895cfc", "#956bff"],\n'
            ")"
        ),
    ),
    ChartEntry(
        name="donut_chart_center_text",
        title="Donut Chart Center Text",
        family="pie",
        render=lambda fn=donut_chart_center_text: fn(),
        snippet=(
            "import reflex_rosencharts as rxc\n\n"
            "rxc.donut_chart_center_text(\n"
            '    data=[{"name": "AAPL", "value": 30}, ...],\n'
            '    center_label="Total",\n'
            '    center_text="184",\n'
            ")"
        ),
    ),
    ChartEntry(
        name="donut_chart_half",
        title="Donut Chart Half",
        family="pie",
        render=lambda fn=donut_chart_half: fn(),
        snippet=(
            "import reflex_rosencharts as rxc\n\n"
            "rxc.donut_chart_half(\n"
            '    data=[{"name": "AAPL", "value": 30}, ...],\n'
            '    colors=["#7e4cfe", "#895cfc"],\n'
            ")"
        ),
    ),
    ChartEntry(
        name="donut_chart_fillable_half",
        title="Donut Chart Fillable Half",
        family="pie",
        render=lambda fn=donut_chart_fillable_half: fn(),
        snippet=(
            "import reflex_rosencharts as rxc\n\n"
            "rxc.donut_chart_fillable_half(\n"
            "    value=72,            # 0-100\n"
            '    label="Goal",\n'
            ")"
        ),
    ),
    ChartEntry(
        name="donut_chart_fillable",
        title="Donut Chart Fillable",
        family="pie",
        render=lambda fn=donut_chart_fillable: fn(),
        snippet=(
            "import reflex_rosencharts as rxc\n\n"
            "rxc.donut_chart_fillable(\n"
            "    value=72,            # 0-100\n"
            '    label="Filled",\n'
            ")"
        ),
    ),
]
