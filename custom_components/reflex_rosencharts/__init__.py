"""reflex-rosencharts: a port of rosencharts to Reflex components.

Public API:
    import reflex_rosencharts as rxc
    rxc.line_chart(data=...)

All 43 charts across 8 families (area, bar, line, pie, scatter, radar, treemap,
other) are re-exported here. See specs/api/component-api-v1.md for the catalog.
"""

__version__ = "0.2.0"

# Shared base wrapper (concrete charts subclass this).
from .reflex_rosencharts import RosenChart, rosen_chart  # noqa: F401

# All ported charts, by family.
from .components.area import *  # noqa: F401,F403
from .components.bar import *  # noqa: F401,F403
from .components.line import *  # noqa: F401,F403
from .components.pie import *  # noqa: F401,F403
from .components.scatter import *  # noqa: F401,F403
from .components.radar import *  # noqa: F401,F403
from .components.treemap import *  # noqa: F401,F403
from .components.other import *  # noqa: F401,F403

from .components import (  # noqa: F401
    area,
    bar,
    line,
    other,
    pie,
    radar,
    scatter,
    treemap,
)

__all__ = [
    "RosenChart",
    "rosen_chart",
    *area.__all__,
    *bar.__all__,
    *line.__all__,
    *pie.__all__,
    *scatter.__all__,
    *radar.__all__,
    *treemap.__all__,
    *other.__all__,
]
