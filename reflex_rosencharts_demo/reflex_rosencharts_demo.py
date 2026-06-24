"""Demo app / gallery showcasing the reflex-rosencharts custom component.

Run it from the project root with:  reflex run

Each chart is fed from ``rx.State`` to demonstrate the Python -> chart data
binding. Use the "Regenerate data" button to push new datasets to every chart.
"""

import random
from datetime import date, timedelta

import reflex as rx

import reflex_rosencharts as rxc

from rxconfig import config

filename = f"{config.app_name}/{config.app_name}.py"


def _time_series(n: int = 16, start: float = 6.0) -> list[dict]:
    """A random-walk [{date, value}] series, the schema area/line charts expect."""
    base = date(2023, 5, 1)
    value = start
    out: list[dict] = []
    for i in range(n):
        value = max(1.0, value + random.uniform(-3, 4))
        out.append({"date": (base + timedelta(days=i)).isoformat(), "value": round(value, 1)})
    return out


def _categories(keys: list[str]) -> list[dict]:
    """A [{key, value}] dataset for the bar chart."""
    return [{"key": k, "value": round(random.uniform(5, 40), 1)} for k in keys]


def _breakdown(names: list[str]) -> list[dict]:
    """A [{name, value}] dataset for the pie chart."""
    return [{"name": n, "value": random.randint(40, 800)} for n in names]


class State(rx.State):
    """Demo state: one dataset per chart, regenerated on demand."""

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
        """Push brand-new datasets to every chart."""
        self.area_data = _time_series(24, 6)
        self.line_data = _time_series(10, 5)
        self.bar_data = _categories(
            ["Technology", "Financials", "Energy", "Cyclical", "Defensive", "Utilities"]
        )
        self.pie_data = _breakdown(
            ["Rent", "Food", "Household", "Transportation", "Entertainment", "Other"]
        )


def chart_card(title: str, subtitle: str, chart: rx.Component) -> rx.Component:
    """A titled card wrapping a single chart."""
    return rx.card(
        rx.vstack(
            rx.heading(title, size="4"),
            rx.text(subtitle, size="2", color_scheme="gray"),
            rx.box(chart, width="100%", padding_top="1rem"),
            spacing="1",
            width="100%",
        ),
        width="100%",
    )


def index() -> rx.Component:
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("reflex-rosencharts", size="9"),
            rx.text(
                "Charts from ",
                rx.code(f"reflex-rosencharts v{rxc.__version__}"),
                ", rendered from pure Python with data from ",
                rx.code("rx.State"),
                ".",
                size="4",
            ),
            rx.button(
                rx.icon("refresh-cw", size=16),
                "Regenerate data",
                on_click=State.regenerate,
                size="3",
            ),
            rx.grid(
                chart_card(
                    "Area chart",
                    "rxc.area_chart — list[{date, value}]",
                    rxc.area_chart(data=State.area_data),
                ),
                chart_card(
                    "Line chart",
                    "rxc.line_chart — list[{date, value}]",
                    rxc.line_chart(data=State.line_data),
                ),
                chart_card(
                    "Horizontal bar chart",
                    "rxc.bar_chart_horizontal — list[{key, value}]",
                    rxc.bar_chart_horizontal(data=State.bar_data),
                ),
                chart_card(
                    "Pie chart",
                    "rxc.pie_chart — list[{name, value}]",
                    rxc.pie_chart(data=State.pie_data),
                ),
                columns=rx.breakpoints(initial="1", md="2"),
                spacing="4",
                width="100%",
            ),
            rx.link(
                rx.button("Reflex custom components docs", variant="soft"),
                href="https://reflex.dev/docs/custom-components/overview/",
                is_external=True,
            ),
            spacing="5",
            width="100%",
            padding_y="3rem",
        ),
        size="4",
    )


app = rx.App()
app.add_page(index)
