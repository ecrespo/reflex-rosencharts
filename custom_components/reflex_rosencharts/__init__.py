"""reflex-rosencharts: a port of rosencharts to Reflex components.

Public API (to be populated during implementation, see specs/api/component-api-v1.md):
    import reflex_rosencharts as rxc
    rxc.line_chart(data=...)

For now the package exposes the scaffold and the demo app. The chart functions
will be re-exported here as they are ported (phases F1-F7 of the plan).
"""

__version__ = "0.2.0"

# Shared base wrapper (concrete charts subclass this).
from .reflex_rosencharts import RosenChart, rosen_chart  # noqa: F401

# Ported charts (one per family so far).
from .components.area import AreaChart, area_chart  # noqa: F401
from .components.bar import BarChartHorizontal, bar_chart_horizontal  # noqa: F401
from .components.line import LineChart, line_chart  # noqa: F401
from .components.pie import PieChart, pie_chart  # noqa: F401

__all__ = [
    "RosenChart",
    "rosen_chart",
    # area
    "AreaChart",
    "area_chart",
    # bar
    "BarChartHorizontal",
    "bar_chart_horizontal",
    # line
    "LineChart",
    "line_chart",
    # pie
    "PieChart",
    "pie_chart",
]
