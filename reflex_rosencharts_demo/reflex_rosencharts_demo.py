"""Demo app showcasing the reflex-rosencharts custom component.

Run it from the project root with:  reflex run

As charts are ported (phases F1-F7), import them here and render them on the page,
e.g.::

    import reflex_rosencharts as rxc
    ...
    rxc.line_chart(data=State.sales, height="18rem")
"""

import reflex as rx

from rxconfig import config

import reflex_rosencharts as rxc

filename = f"{config.app_name}/{config.app_name}.py"


class State(rx.State):
    """The demo app state."""


def index() -> rx.Component:
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("reflex-rosencharts", size="9"),
            rx.text(
                "Custom component scaffold ",
                rx.code(f"v{rxc.__version__}"),
                ". Edit ",
                rx.code(filename),
                " and add charts as they are ported.",
                size="5",
            ),
            rx.link(
                rx.button("Reflex custom components docs"),
                href="https://reflex.dev/docs/custom-components/overview/",
                is_external=True,
            ),
            spacing="5",
            justify="center",
            min_height="85vh",
        ),
    )


app = rx.App()
app.add_page(index)