"""Shell shared by every page: navbar, page header and the event log panel."""

from __future__ import annotations

import reflex as rx

from .state import LogState

PAGES = [
    ("/", "Basico"),
    ("/controlado", "Controlado"),
    ("/tema", "Tema y locale"),
    ("/avanzado", "Avanzado"),
]


def navbar() -> rx.Component:
    """The top navigation, and the target of the first step of every tour."""
    return rx.hstack(
        rx.hstack(
            rx.icon("route", size=22, color=rx.color("violet", 10)),
            rx.heading("reflex-react-joyride", size="4"),
            align="center",
            spacing="2",
            id="nav-logo",
        ),
        rx.spacer(),
        rx.hstack(
            *[rx.link(label, href=href, size="2", weight="medium") for href, label in PAGES],
            spacing="5",
            id="nav-links",
        ),
        rx.color_mode.button(size="1"),
        width="100%",
        align="center",
        spacing="4",
        padding="1rem 1.5rem",
        border_bottom=f"1px solid {rx.color('gray', 5)}",
        background=rx.color("gray", 1),
        position="sticky",
        top="0",
        z_index="50",
    )


def page_header(title: str, description: str) -> rx.Component:
    """Title and one-line description."""
    return rx.vstack(
        rx.heading(title, size="7"),
        rx.text(description, color=rx.color("gray", 11), size="3"),
        align="start",
        spacing="2",
        width="100%",
    )


def control_dock(*actions: rx.Component) -> rx.Component:
    """The buttons that drive the tour.

    react-joyride's overlay covers the page while a step is open, so anything
    meant to stay clickable during a tour has to sit above it: this dock uses a
    z-index higher than the tour's ``z_index`` option.
    """
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.icon("route", size=14, color=rx.color("violet", 10)),
                rx.text("Controles del tour", size="1", weight="medium", color=rx.color("gray", 11)),
                spacing="2",
                align="center",
            ),
            rx.hstack(*actions, spacing="2", wrap="wrap", align="center"),
            spacing="2",
            align="start",
        ),
        position="fixed",
        bottom="1.25rem",
        left="1.25rem",
        z_index="1200",
        box_shadow="0 12px 32px rgba(15, 23, 42, 0.22)",
        max_width="min(92vw, 560px)",
    )


def event_log() -> rx.Component:
    """A live view of what react-joyride is emitting."""
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.heading("Eventos", size="3"),
                rx.spacer(),
                rx.button("Limpiar", size="1", variant="soft", on_click=LogState.clear),
                width="100%",
                align="center",
            ),
            rx.cond(
                LogState.log,
                rx.vstack(
                    rx.foreach(
                        LogState.log,
                        lambda line: rx.text(
                            line, size="1", font_family="monospace", color=rx.color("gray", 11)
                        ),
                    ),
                    spacing="1",
                    align="start",
                    width="100%",
                ),
                rx.text("Sin eventos todavia. Inicia el tour.", size="1", color=rx.color("gray", 9)),
            ),
            spacing="3",
            width="100%",
            align="start",
        ),
        width="100%",
        id="event-log",
    )


def shell(title: str, description: str, actions: list[rx.Component], *content: rx.Component) -> rx.Component:
    """Compose a page: navbar, header, content and the event log."""
    return rx.box(
        # react-joyride renders into document.body by default, which paints above
        # Reflex's Radix theme root (a stacking context with z-index 0). Giving
        # the tour a portal inside the app puts the overlay and the dock in the
        # same stacking context, so the dock's z-index can win.
        rx.box(id="tour-root"),
        navbar(),
        rx.container(
            rx.vstack(
                page_header(title, description),
                *content,
                event_log(),
                rx.box(height="6rem"),
                spacing="6",
                width="100%",
                align="start",
            ),
            size="3",
            padding_y="2rem",
        ),
        control_dock(*actions),
        min_height="100vh",
        background=rx.color("gray", 2),
    )
