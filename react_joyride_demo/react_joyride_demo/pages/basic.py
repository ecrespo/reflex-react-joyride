"""Page 1 - the shortest possible tour.

A continuous tour driven by a single boolean in the State, plus the imperative
helpers (``rjr.go_to``, ``rjr.skip``) that talk to the running tour directly.
"""

from __future__ import annotations

import reflex as rx
import reflex_react_joyride as rjr

from ..layout import shell
from ..state import LogState

TOUR_ID = "basico"

STEPS = [
    rjr.Step(
        target="#nav-logo",
        title="Bienvenido",
        content="Este tour recorre una pantalla tipica en cuatro pasos. Cierra el tooltip o pulsa Siguiente.",
        placement="bottom-start",
    ),
    rjr.Step(
        target="#basic-search",
        title="Busqueda",
        content="El spotlight recorta el overlay sobre el elemento, y el tooltip se reposiciona solo si no hay espacio.",
        placement="bottom",
    ),
    rjr.Step(
        target="#basic-stats",
        title="Metricas",
        content="Cada paso puede sobreescribir las opciones del tour: este usa mas padding en el spotlight.",
        placement="top",
        spotlight_padding=16,
    ),
    rjr.Step(
        target="#basic-cta",
        title="Listo",
        content="Ultimo paso: el boton primario dice 'Listo' y al pulsarlo se emite tour:end.",
        placement="left",
        data={"final": True},
    ),
]


class BasicState(rx.State):
    """Runs the tour of the first page."""

    run: bool = False
    completed: bool = False

    @rx.event
    def start(self):
        """Start the tour from the first step."""
        self.completed = False
        self.run = True

    @rx.event
    def finish(self, event: rjr.JoyrideEvent):
        """Stop the tour when react-joyride says it is over."""
        self.run = False
        self.completed = event["status"] == rjr.STATUS.FINISHED


def stat_card(label: str, value: str, delta: str, icon: str) -> rx.Component:
    return rx.card(
        rx.hstack(
            rx.icon(icon, size=18, color=rx.color("violet", 10)),
            rx.vstack(
                rx.text(label, size="1", color=rx.color("gray", 11)),
                rx.heading(value, size="5"),
                rx.text(delta, size="1", color=rx.color("grass", 11)),
                spacing="0",
                align="start",
            ),
            spacing="3",
            align="center",
        ),
        width="100%",
    )


@rx.page(route="/", title="reflex-react-joyride - tour basico")
def basic_page() -> rx.Component:
    """A four step tour over a small fake dashboard."""
    return shell(
        "Tour basico",
        "Un tour continuo que se enciende y se apaga con un booleano del State.",
        [
            rx.button(
                rx.icon("play", size=16),
                "Iniciar tour",
                on_click=BasicState.start,
                disabled=BasicState.run,
            ),
            rx.button(
                "Ir al paso 3", variant="soft", on_click=rjr.go_to(TOUR_ID, 2), disabled=~BasicState.run
            ),
            rx.button(
                "Saltar",
                variant="soft",
                color_scheme="gray",
                on_click=rjr.skip(TOUR_ID),
                disabled=~BasicState.run,
            ),
            rx.cond(
                BasicState.completed,
                rx.badge("Tour completado", color_scheme="grass", size="2"),
                rx.fragment(),
            ),
        ],
        rjr.joyride(
            tour_id=TOUR_ID,
            steps=STEPS,
            portal_element="#tour-root",
            run=BasicState.run,
            continuous=True,
            options=rjr.TourOptions(
                show_progress=True,
                primary_color=rx.color("violet", 9),
                buttons=["back", "skip", "primary"],
                z_index=1000,
            ),
            on_event=LogState.record,
            on_tour_end=BasicState.finish,
        ),
        rx.card(
            rx.vstack(
                rx.input(
                    placeholder="Buscar clientes, facturas, pedidos...",
                    id="basic-search",
                    width="100%",
                ),
                rx.grid(
                    stat_card("Ingresos", "48.2k", "+12% vs. mes pasado", "trending-up"),
                    stat_card("Clientes", "1.284", "+48 nuevos", "users"),
                    stat_card("Tickets", "23", "-8 abiertos", "bell"),
                    columns="3",
                    spacing="3",
                    width="100%",
                    id="basic-stats",
                ),
                rx.hstack(
                    rx.text("Todo listo para el cierre de mes.", size="2", color=rx.color("gray", 11)),
                    rx.spacer(),
                    rx.button("Generar reporte", id="basic-cta"),
                    width="100%",
                    align="center",
                ),
                spacing="4",
                width="100%",
            ),
            width="100%",
        ),
    )
