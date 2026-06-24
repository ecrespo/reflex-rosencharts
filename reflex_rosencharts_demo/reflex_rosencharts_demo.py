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
        out.append({"date": (base + timedelta(days=i)).isoformat(), "value": round(value, 1)})
    return out


def _categories(keys: list[str]) -> list[dict]:
    return [{"key": k, "value": round(random.uniform(5, 40), 1)} for k in keys]


def _breakdown(names: list[str]) -> list[dict]:
    return [{"name": n, "value": random.randint(40, 800)} for n in names]


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
    ("Area", [
        ("area_chart", rxc.area_chart),
        ("area_chart_full", rxc.area_chart_full),
        ("area_chart_gradient", rxc.area_chart_gradient),
        ("area_chart_semi_filled", rxc.area_chart_semi_filled),
    ]),
    ("Bar", [
        ("bar_chart_horizontal", rxc.bar_chart_horizontal),
        ("bar_chart_horizontal_logo", rxc.bar_chart_horizontal_logo),
        ("bar_chart_gradient", rxc.bar_chart_gradient),
        ("bar_chart_breakdown", rxc.bar_chart_breakdown),
        ("bar_chart_thin_breakdown", rxc.bar_chart_thin_breakdown),
        ("bar_chart_thin_horizontal", rxc.bar_chart_thin_horizontal),
        ("bar_chart_flags_horizontal", rxc.bar_chart_flags_horizontal),
        ("bar_chart_vertical", rxc.bar_chart_vertical),
        ("bar_chart_multi_vertical", rxc.bar_chart_multi_vertical),
        ("bar_chart_triple_flags_horizontal", rxc.bar_chart_triple_flags_horizontal),
        ("bar_chart_line", rxc.bar_chart_line),
        ("bar_chart_benchmark", rxc.bar_chart_benchmark),
    ]),
    ("Line", [
        ("line_chart", rxc.line_chart),
        ("line_chart_curved", rxc.line_chart_curved),
        ("line_chart_multiple", rxc.line_chart_multiple),
        ("line_chart_labels_curved", rxc.line_chart_labels_curved),
        ("line_chart_stocks_curved", rxc.line_chart_stocks_curved),
        ("line_chart_step", rxc.line_chart_step),
        ("line_chart_pulse", rxc.line_chart_pulse),
        ("line_chart_full", rxc.line_chart_full),
    ]),
    ("Pie / Donut", [
        ("pie_chart", rxc.pie_chart),
        ("pie_chart_stocks", rxc.pie_chart_stocks),
        ("pie_chart_labels", rxc.pie_chart_labels),
        ("donut_chart", rxc.donut_chart),
        ("donut_chart_center_text", rxc.donut_chart_center_text),
        ("donut_chart_half", rxc.donut_chart_half),
        ("donut_chart_fillable_half", rxc.donut_chart_fillable_half),
        ("donut_chart_fillable", rxc.donut_chart_fillable),
    ]),
    ("Scatter", [
        ("scatter_chart", rxc.scatter_chart),
        ("scatter_chart_interactive", rxc.scatter_chart_interactive),
        ("scatter_chart_multiclass", rxc.scatter_chart_multiclass),
        ("scatter_chart_stocks", rxc.scatter_chart_stocks),
    ]),
    ("Radar", [
        ("radar_chart", rxc.radar_chart),
        ("radar_chart_rounded", rxc.radar_chart_rounded),
    ]),
    ("Treemap", [
        ("treemap_chart", rxc.treemap_chart),
        ("treemap_chart_images", rxc.treemap_chart_images),
        ("treemap_chart_gradient", rxc.treemap_chart_gradient),
    ]),
    ("Other", [
        ("bubble_chart", rxc.bubble_chart),
        ("funnel_chart", rxc.funnel_chart),
    ]),
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
            *[
                chart_card(fn_name, f"rxc.{fn_name}()", fn())
                for fn_name, fn in charts
            ],
            columns=rx.breakpoints(initial="1", sm="2", lg="3"),
            spacing="4",
            width="100%",
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
                chart_card("Area", "rxc.area_chart(data=State.area_data)", rxc.area_chart(data=State.area_data)),
                chart_card("Line", "rxc.line_chart(data=State.line_data)", rxc.line_chart(data=State.line_data)),
                chart_card("Bar", "rxc.bar_chart_horizontal(data=State.bar_data)", rxc.bar_chart_horizontal(data=State.bar_data)),
                chart_card("Pie", "rxc.pie_chart(data=State.pie_data)", rxc.pie_chart(data=State.pie_data)),
                columns=rx.breakpoints(initial="1", md="2"),
                spacing="4",
                width="100%",
            ),
            rx.divider(margin_y="1.5rem"),
            rx.heading("Full catalog (43 charts)", size="7"),
            rx.text("Each chart rendered with its built-in example dataset.", size="2", color_scheme="gray"),
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
