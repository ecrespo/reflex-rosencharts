"""reflex-rosencharts demo gallery.

Renders one example card per ported chart, grouped by family, with a sidebar for
navigation and a Python usage snippet beside each chart. This is the "examples"
surface of the library and the visual test bench (one card per chart).
"""

import reflex as rx

from .gallery.registry import ChartEntry, FAMILIES, all_entries


def _chart_card(entry: ChartEntry) -> rx.Component:
    """A single gallery card: title, rendered chart, and usage snippet."""
    return rx.box(
        rx.heading(entry.title, size="4", margin_bottom="0.5rem"),
        rx.box(
            entry.render(),
            width="100%",
            padding="1rem",
            border="1px solid var(--gray-4)",
            border_radius="0.5rem",
            background="var(--color-background)",
        ),
        rx.code_block(
            entry.snippet,
            language="python",
            margin_top="0.75rem",
            width="100%",
            font_size="0.8rem",
        ),
        id=entry.name,
        width="100%",
        padding="1.25rem",
        border="1px solid var(--gray-3)",
        border_radius="0.75rem",
        margin_bottom="1.5rem",
    )


def _family_section(
    family_key: str, family_label: str, entries: list[ChartEntry]
) -> rx.Component:
    """A family heading followed by its chart cards (or a 'pending' note)."""
    if not entries:
        body: rx.Component = rx.text(
            "Pendiente de portar.", color="var(--gray-9)", font_style="italic"
        )
    else:
        body = rx.vstack(
            *[_chart_card(e) for e in entries], width="100%", spacing="0"
        )
    return rx.box(
        rx.heading(family_label, size="6", margin_bottom="1rem"),
        body,
        id=f"family-{family_key}",
        width="100%",
        margin_bottom="2.5rem",
    )


def _sidebar(entries_by_family: dict[str, list[ChartEntry]]) -> rx.Component:
    """Sticky sidebar listing families with a count of ported charts."""
    links = []
    for key, label in FAMILIES:
        count = len(entries_by_family.get(key, []))
        links.append(
            rx.link(
                f"{label} ({count})",
                href=f"#family-{key}",
                display="block",
                padding_y="0.35rem",
                color="var(--gray-11)",
            )
        )
    return rx.box(
        rx.heading("rosencharts", size="5", margin_bottom="0.25rem"),
        rx.text(
            "Reflex port",
            color="var(--gray-9)",
            font_size="0.85rem",
            margin_bottom="1rem",
        ),
        *links,
        position="sticky",
        top="1rem",
        height="fit-content",
        min_width="14rem",
        padding="1rem",
    )


def index() -> rx.Component:
    """Gallery page: sidebar + all family sections."""
    entries_by_family = all_entries()
    total = sum(len(v) for v in entries_by_family.values())
    sections = [
        _family_section(key, label, entries_by_family.get(key, []))
        for key, label in FAMILIES
    ]
    return rx.box(
        rx.color_mode.button(position="top-right"),
        rx.hstack(
            _sidebar(entries_by_family),
            rx.box(
                rx.heading(
                    f"reflex-rosencharts — galería ({total}/43)",
                    size="8",
                    margin_bottom="1.5rem",
                ),
                *sections,
                width="100%",
                max_width="56rem",
                padding="1.5rem",
            ),
            align="start",
            width="100%",
            spacing="4",
        ),
        width="100%",
    )


app = rx.App()
app.add_page(index, route="/")
