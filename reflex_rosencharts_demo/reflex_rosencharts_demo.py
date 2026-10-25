"""Demo app / gallery showcasing the reflex-rosencharts custom component.

Run it from the project root with:  reflex run

Two sections:
  1. Featured charts fed from rx.State (with a "Regenerate data" button) to show
     the Python -> chart data binding.
  2. Full catalog: all 43 charts across 8 families, each rendered with its
     built-in example dataset (call the function with no args).
"""

import random
from datetime import date, timedelta

import reflex as rx

import reflex_rosencharts as rxc

from rxconfig import config

filename = f"{config.app_name}/{config.app_name}.py"


def _time_series(n: int = 16, start: float = 6.0) -> list[dict]:
    base = date(2023, 5, 1)
    value = start
    out: list[dict] = []
    for i in range(n):
        value = max(1.0, value + random.uniform(-3, 4))
        out.append(
            {"date": (base + timedelta(days=i)).isoformat(), "value": round(value, 1)}
        )
    return out


def _categories(keys: list[str]) -> list[dict]:
    return [{"key": k, "value": round(random.uniform(5, 40), 1)} for k in keys]


def _breakdown(names: list[str]) -> list[dict]:
    return [{"name": n, "value": random.randint(40, 800)} for n in names]


# Real-world, clustered data: days alive vs. number of commits for 13 GitHub
# repositories. Most are young and small, two are old, one has ten times the
# commits of the rest. This is the shape of data that exposed the scatter axis
# defects fixed in 0.2.2: irregular and overlapping x labels, extreme points cut
# in half, and a chart that silently depended on the input order.
REPO_STATS: list[dict] = [
    {"company": "omagnome", "revenue": 1, "value": 53},
    {"company": "reflex-mapcn", "revenue": 1, "value": 38},
    {"company": "mcp-joke-server", "revenue": 1, "value": 34},
    {"company": "fastapi_todos", "revenue": 16, "value": 43},
    {"company": "vigia-eew", "revenue": 19, "value": 46},
    {"company": "quiz", "revenue": 28, "value": 47},
    {"company": "prismal", "revenue": 143, "value": 440},
    {"company": "python-android_sms", "revenue": 229, "value": 138},
    {"company": "ecrespo-localpaquetes", "revenue": 273, "value": 46},
    {"company": "reflex_resume", "revenue": 287, "value": 50},
    {"company": "python-autoaccesibilidad", "revenue": 403, "value": 49},
    {"company": "tutorial_fastAPI", "revenue": 1409, "value": 45},
    {"company": "pysms-send", "revenue": 2345, "value": 29},
]

# The extreme case: the oldest repo, with 10x the commits of any other.
REPO_OUTLIER: dict = {"company": "ecrespo.github.io", "revenue": 2609, "value": 1451}


class State(rx.State):
    """Demo state: datasets for the featured charts, regenerated on demand."""

    area_data: list[dict] = _time_series(24, 6)
    line_data: list[dict] = _time_series(10, 5)
    bar_data: list[dict] = _categories(
        ["Technology", "Financials", "Energy", "Cyclical", "Defensive", "Utilities"]
    )
    pie_data: list[dict] = _breakdown(
        ["Rent", "Food", "Household", "Transportation", "Entertainment", "Other"]
    )

    # Scatter-axes demo (see REPO_STATS above).
    repo_scatter: list[dict] = list(REPO_STATS)
    scatter_scale: str = "linear"
    scatter_has_outlier: bool = False

    @rx.event
    def shuffle_repo_scatter(self):
        """Same chart, same tooltips: the axes no longer depend on the order."""
        data = list(self.repo_scatter)
        random.shuffle(data)
        self.repo_scatter = data

    @rx.event
    def set_outlier(self, value: bool):
        self.scatter_has_outlier = value
        self.repo_scatter = list(REPO_STATS) + ([REPO_OUTLIER] if value else [])

    @rx.event
    def set_scatter_scale(self, value: str):
        self.scatter_scale = value

    @rx.event
    def regenerate(self):
        self.area_data = _time_series(24, 6)
        self.line_data = _time_series(10, 5)
        self.bar_data = _categories(
            ["Technology", "Financials", "Energy", "Cyclical", "Defensive", "Utilities"]
        )
        self.pie_data = _breakdown(
            ["Rent", "Food", "Household", "Transportation", "Entertainment", "Other"]
        )


# Full catalog: family -> list of (title, function). All rendered with defaults.
CATALOG: list[tuple[str, list[tuple[str, callable]]]] = [
    (
        "Area",
        [
            ("area_chart", rxc.area_chart),
            ("area_chart_full", rxc.area_chart_full),
            ("area_chart_gradient", rxc.area_chart_gradient),
            ("area_chart_semi_filled", rxc.area_chart_semi_filled),
        ],
    ),
    (
        "Bar",
        [
            ("bar_chart_horizontal", rxc.bar_chart_horizontal),
            ("bar_chart_horizontal_logo", rxc.bar_chart_horizontal_logo),
            ("bar_chart_gradient", rxc.bar_chart_gradient),
            ("bar_chart_breakdown", rxc.bar_chart_breakdown),
            ("bar_chart_thin_breakdown", rxc.bar_chart_thin_breakdown),
            ("bar_chart_thin_horizontal", rxc.bar_chart_thin_horizontal),
            ("bar_chart_flags_horizontal", rxc.bar_chart_flags_horizontal),
            ("bar_chart_vertical", rxc.bar_chart_vertical),
            ("bar_chart_multi_vertical", rxc.bar_chart_multi_vertical),
            (
                "bar_chart_triple_flags_horizontal",
                rxc.bar_chart_triple_flags_horizontal,
            ),
            ("bar_chart_line", rxc.bar_chart_line),
            ("bar_chart_benchmark", rxc.bar_chart_benchmark),
        ],
    ),
    (
        "Line",
        [
            ("line_chart", rxc.line_chart),
            ("line_chart_curved", rxc.line_chart_curved),
            ("line_chart_multiple", rxc.line_chart_multiple),
            ("line_chart_labels_curved", rxc.line_chart_labels_curved),
            ("line_chart_stocks_curved", rxc.line_chart_stocks_curved),
            ("line_chart_step", rxc.line_chart_step),
            ("line_chart_pulse", rxc.line_chart_pulse),
            ("line_chart_full", rxc.line_chart_full),
        ],
    ),
    (
        "Pie / Donut",
        [
            ("pie_chart", rxc.pie_chart),
            ("pie_chart_stocks", rxc.pie_chart_stocks),
            ("pie_chart_labels", rxc.pie_chart_labels),
            ("donut_chart", rxc.donut_chart),
            ("donut_chart_center_text", rxc.donut_chart_center_text),
            ("donut_chart_half", rxc.donut_chart_half),
            ("donut_chart_fillable_half", rxc.donut_chart_fillable_half),
            ("donut_chart_fillable", rxc.donut_chart_fillable),
        ],
    ),
    (
        "Scatter",
        [
            ("scatter_chart", rxc.scatter_chart),
            ("scatter_chart_interactive", rxc.scatter_chart_interactive),
            ("scatter_chart_multiclass", rxc.scatter_chart_multiclass),
            ("scatter_chart_stocks", rxc.scatter_chart_stocks),
        ],
    ),
    (
        "Radar",
        [
            ("radar_chart", rxc.radar_chart),
            ("radar_chart_rounded", rxc.radar_chart_rounded),
        ],
    ),
    (
        "Treemap",
        [
            ("treemap_chart", rxc.treemap_chart),
            ("treemap_chart_images", rxc.treemap_chart_images),
            ("treemap_chart_gradient", rxc.treemap_chart_gradient),
        ],
    ),
    (
        "Other",
        [
            ("bubble_chart", rxc.bubble_chart),
            ("funnel_chart", rxc.funnel_chart),
        ],
    ),
]


def chart_card(title: str, subtitle: str, chart: rx.Component) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.heading(title, size="3"),
            rx.text(subtitle, size="1", color_scheme="gray"),
            rx.box(chart, width="100%", padding_top="0.75rem"),
            spacing="1",
            width="100%",
        ),
        width="100%",
    )


def family_section(name: str, charts: list[tuple[str, callable]]) -> rx.Component:
    return rx.vstack(
        rx.heading(name, size="6", margin_top="1rem"),
        rx.grid(
            *[chart_card(fn_name, f"rxc.{fn_name}()", fn()) for fn_name, fn in charts],
            columns=rx.breakpoints(initial="1", sm="2", lg="3"),
            spacing="4",
            width="100%",
        ),
        spacing="3",
        width="100%",
        align="start",
    )


def scatter_axes_section() -> rx.Component:
    """The 0.2.2 axis fixes, shown on data that used to break them."""
    chart = rxc.scatter_chart(data=State.repo_scatter, x_scale=State.scatter_scale)
    narrow = rxc.scatter_chart(data=State.repo_scatter, x_scale=State.scatter_scale)
    return rx.vstack(
        rx.heading("Scatter axes on clustered data", size="6", margin_top="1rem"),
        rx.text(
            "Days alive vs. commits for 13 repositories. The x labels are regular ticks that "
            "line up with the grid lines, both domains come from the extent of the data instead "
            "of its first and last element, no point is clipped at the edges, and the y gutter "
            "grows with the longest label.",
            size="2",
            color_scheme="gray",
        ),
        rx.hstack(
            rx.button(
                rx.icon("shuffle", size=16),
                "Shuffle order",
                on_click=State.shuffle_repo_scatter,
                size="2",
                variant="soft",
            ),
            rx.hstack(
                rx.switch(
                    checked=State.scatter_has_outlier, on_change=State.set_outlier
                ),
                rx.text("Add the extreme point", size="2"),
                spacing="2",
                align="center",
            ),
            rx.hstack(
                rx.text("x scale", size="2"),
                rx.select(
                    ["linear", "log", "symlog"],
                    value=State.scatter_scale,
                    on_change=State.set_scatter_scale,
                ),
                spacing="2",
                align="center",
            ),
            spacing="5",
            align="center",
            wrap="wrap",
            width="100%",
        ),
        chart_card(
            "Full width",
            "rxc.scatter_chart(data=State.repo_scatter, x_scale=State.scatter_scale)",
            chart,
        ),
        rx.box(
            chart_card("At 390px", "the same chart at phone width", narrow),
            width="390px",
            max_width="100%",
        ),
        spacing="3",
        width="100%",
        align="start",
    )


# Monthly series whose maximum (June) sits two points before the last one: at
# phone width its label used to land on top of the last one ("6/19/1").
DEV_STATS = [
    {"date": f"{year}-{month:02d}-01T00:00:00", "value": value}
    for year, values in {
        2024: [0, 0, 8, 0, 22, 8, 23, 12, 17, 19, 5, 8],
        2025: [3, 10, 1, 0, 0, 9, 7, 21, 10, 41, 66, 34],
        2026: [9, 94, 130, 59, 66, 193, 85, 61, 81],
    }.items()
    for month, value in enumerate(values, start=1)
]


def x_labels_section() -> rx.Component:
    """The 0.2.4 x-axis fix: labels that do not fit are dropped, never overlapped."""
    return rx.vstack(
        rx.heading("X labels that never overlap", size="6", margin_top="1rem"),
        rx.text(
            "The line and area charts label the first point, the last point and the maximum. "
            "When the maximum sits close to an edge its label is dropped instead of being drawn "
            "on top of another one; resize the window to see the labels recomputed.",
            size="2",
            color_scheme="gray",
        ),
        rx.grid(
            chart_card(
                "Full width",
                "rxc.line_chart_pulse(data=DEV_STATS)",
                rxc.line_chart_pulse(data=DEV_STATS),
            ),
            chart_card(
                "Regular ticks",
                'rxc.line_chart_pulse(data=DEV_STATS, x_ticks="regular")',
                rxc.line_chart_pulse(data=DEV_STATS, x_ticks="regular"),
            ),
            columns=rx.breakpoints(initial="1", md="2"),
            spacing="4",
            width="100%",
        ),
        rx.box(
            chart_card(
                "At 390px",
                "the same chart at phone width",
                rxc.line_chart_pulse(data=DEV_STATS),
            ),
            id="x-labels-narrow",
            width="390px",
            max_width="100%",
        ),
        spacing="3",
        width="100%",
        align="start",
    )


def index() -> rx.Component:
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("reflex-rosencharts", size="9"),
            rx.text(
                "All 43 rosencharts charts, rendered from pure Python via ",
                rx.code(f"reflex-rosencharts v{rxc.__version__}"),
                ".",
                size="4",
            ),
            # Featured (state-driven) section.
            rx.heading("Featured — data from rx.State", size="6", margin_top="1rem"),
            rx.button(
                rx.icon("refresh-cw", size=16),
                "Regenerate data",
                on_click=State.regenerate,
                size="3",
            ),
            rx.grid(
                chart_card(
                    "Area",
                    "rxc.area_chart(data=State.area_data)",
                    rxc.area_chart(data=State.area_data),
                ),
                chart_card(
                    "Line",
                    "rxc.line_chart(data=State.line_data)",
                    rxc.line_chart(data=State.line_data),
                ),
                chart_card(
                    "Bar",
                    "rxc.bar_chart_horizontal(data=State.bar_data)",
                    rxc.bar_chart_horizontal(data=State.bar_data),
                ),
                chart_card(
                    "Pie",
                    "rxc.pie_chart(data=State.pie_data)",
                    rxc.pie_chart(data=State.pie_data),
                ),
                columns=rx.breakpoints(initial="1", md="2"),
                spacing="4",
                width="100%",
            ),
            rx.divider(margin_y="1.5rem"),
            scatter_axes_section(),
            rx.divider(margin_y="1.5rem"),
            x_labels_section(),
            rx.divider(margin_y="1.5rem"),
            rx.heading("Full catalog (43 charts)", size="7"),
            rx.text(
                "Each chart rendered with its built-in example dataset.",
                size="2",
                color_scheme="gray",
            ),
            *[family_section(name, charts) for name, charts in CATALOG],
            rx.link(
                rx.button("Reflex custom components docs", variant="soft"),
                href="https://reflex.dev/docs/custom-components/overview/",
                is_external=True,
                margin_top="2rem",
            ),
            spacing="4",
            width="100%",
            padding_y="3rem",
            align="start",
        ),
        size="4",
    )


app = rx.App()
app.add_page(index)
