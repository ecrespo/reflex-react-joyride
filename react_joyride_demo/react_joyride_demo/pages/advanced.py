"""Page 4 - the cases that make a tour survive a real app.

* a modal-like welcome step (``placement="center"`` on ``body``);
* a target that does not exist yet, waited for with ``target_wait_timeout``;
* a target that never appears, caught by ``on_target_not_found``;
* a spotlight over a different element than the one the tooltip points at;
* a step far below the fold, to watch the scroll events;
* a step that blocks interaction with the highlighted element, and another one
  without overlay and with the ESC key disabled.
"""

from __future__ import annotations

import asyncio

import reflex as rx
import reflex_react_joyride as rjr

from ..layout import shell
from ..state import LogState

TOUR_ID = "avanzado"

STEPS = [
    rjr.Step(
        target="body",
        placement="center",
        title="Un paso modal",
        content="Con placement='center' el paso se centra en la pantalla y no dibuja flecha: ideal para abrir un tour.",
        spotlight_padding=0,
    ),
    rjr.Step(
        target="#adv-async",
        title="Target que aun no existe",
        content="Este elemento tarda dos segundos en aparecer. El tour espera hasta target_wait_timeout antes de rendirse.",
        placement="bottom",
        target_wait_timeout=6000,
    ),
    rjr.Step(
        target="#adv-no-existe",
        title="Este no deberia verse",
        content="Su target no existe: react-joyride emite error:target_not_found y seguimos adelante.",
        target_wait_timeout=1500,
    ),
    rjr.Step(
        target="#adv-toggle",
        spotlight_target="#adv-card",
        title="Spotlight separado",
        content="El tooltip apunta al interruptor, pero el spotlight recorta la tarjeta completa.",
        placement="right",
    ),
    rjr.Step(
        target="#adv-locked",
        title="Interaccion bloqueada",
        content="block_target_interaction impide pulsar el boton resaltado mientras el paso esta abierto.",
        placement="top",
        block_target_interaction=True,
    ),
    rjr.Step(
        target="#adv-footer",
        title="Abajo del todo",
        content="El tour hace scroll hasta aqui: mira scroll:start y scroll:end en el registro de eventos.",
        placement="top",
        scroll_offset=120,
    ),
    rjr.Step(
        target="#adv-quiet",
        title="Sin overlay",
        content="hide_overlay deja la pagina usable, y dismiss_key_action=False desactiva la tecla ESC.",
        placement="top",
        hide_overlay=True,
        dismiss_key_action=False,
    ),
]


class AdvancedState(rx.State):
    """Runs the advanced tour and fakes an async widget."""

    run: bool = False
    loading: bool = False
    loaded: bool = False
    locked_clicks: int = 0
    missing: list[str] = []

    @rx.event(background=True)
    async def start(self):
        """Start the tour and load the async card two seconds later."""
        async with self:
            self.missing = []
            self.loaded = False
            self.loading = True
            self.run = True

        await asyncio.sleep(2)

        async with self:
            self.loading = False
            self.loaded = True

    @rx.event
    def finish(self, _event: rjr.JoyrideEvent):
        self.run = False

    @rx.event
    def target_missing(self, event: rjr.JoyrideEvent):
        """Record the steps whose target never showed up."""
        self.missing = [
            *self.missing,
            f"paso {event['index'] + 1}: {event['step_id'] or event['step_target']}",
        ]

    @rx.event
    def count_click(self):
        self.locked_clicks += 1


@rx.page(route="/avanzado", title="reflex-react-joyride - casos avanzados")
def advanced_page() -> rx.Component:
    """Center placement, waiting targets, spotlight targets, scrolling and more."""
    return shell(
        "Casos avanzados",
        "Pasos modales, targets que tardan o no llegan, spotlight separado, scroll y overlay.",
        [
            rx.button(
                rx.icon("play", size=16),
                "Iniciar tour",
                on_click=AdvancedState.start,
                disabled=AdvancedState.run,
            ),
            rx.button(
                "Repetir paso", variant="soft", on_click=rjr.replay(TOUR_ID), disabled=~AdvancedState.run
            ),
            rx.cond(
                AdvancedState.missing,
                rx.badge(
                    f"Targets no encontrados: {AdvancedState.missing.length()}",
                    color_scheme="tomato",
                    size="2",
                ),
                rx.fragment(),
            ),
        ],
        rjr.joyride(
            tour_id=TOUR_ID,
            steps=STEPS,
            portal_element="#tour-root",
            run=AdvancedState.run,
            continuous=True,
            scroll_to_first_step=True,
            options=rjr.TourOptions(
                show_progress=True,
                skip_beacon=True,
                primary_color=rx.color("violet", 9),
                scroll_offset=80,
                scroll_duration=400,
                z_index=1000,
            ),
            floating_options=rjr.FloatingOptions(shift_options={"padding": 16}),
            on_event=LogState.record,
            on_target_not_found=AdvancedState.target_missing,
            on_tour_end=AdvancedState.finish,
        ),
        rx.grid(
            rx.card(
                rx.vstack(
                    rx.heading("Carga diferida", size="3"),
                    rx.cond(
                        AdvancedState.loaded,
                        rx.vstack(
                            rx.text("Datos listos.", size="2", color=rx.color("grass", 11)),
                            rx.text(
                                "Este bloque aparecio dos segundos tarde.",
                                size="1",
                                color=rx.color("gray", 11),
                            ),
                            spacing="1",
                            align="start",
                            id="adv-async",
                        ),
                        rx.hstack(
                            rx.spinner(size="2"),
                            rx.text("Cargando...", size="2", color=rx.color("gray", 11)),
                            spacing="2",
                            align="center",
                        ),
                    ),
                    spacing="3",
                    align="start",
                    min_height="92px",
                ),
            ),
            rx.card(
                rx.vstack(
                    rx.heading("Spotlight separado", size="3"),
                    rx.text("El recorte cubre toda la tarjeta.", size="1", color=rx.color("gray", 11)),
                    rx.hstack(
                        rx.switch(id="adv-toggle"),
                        rx.text("Notificaciones", size="2"),
                        spacing="2",
                        align="center",
                    ),
                    spacing="3",
                    align="start",
                ),
                id="adv-card",
            ),
            rx.card(
                rx.vstack(
                    rx.heading("Interaccion bloqueada", size="3"),
                    rx.button("No me puedes pulsar", id="adv-locked", on_click=AdvancedState.count_click),
                    rx.text(
                        f"Clics recibidos: {AdvancedState.locked_clicks}",
                        size="1",
                        color=rx.color("gray", 11),
                    ),
                    spacing="3",
                    align="start",
                ),
            ),
            columns="3",
            spacing="4",
            width="100%",
        ),
        rx.card(
            rx.vstack(
                rx.heading("Sin overlay", size="3"),
                rx.text(
                    "La pagina sigue siendo usable mientras este paso esta abierto.",
                    size="2",
                    color=rx.color("gray", 11),
                ),
                spacing="2",
                align="start",
            ),
            id="adv-quiet",
            width="100%",
        ),
        rx.box(
            rx.callout(
                "Desplazate: el ultimo paso de contenido vive aqui abajo.",
                icon="arrow-down",
                color_scheme="gray",
            ),
            height="90vh",
            width="100%",
            display="flex",
            align_items="center",
            justify_content="center",
        ),
        rx.card(
            rx.vstack(
                rx.heading("Fin del recorrido", size="3"),
                rx.text(
                    "El tour hizo scroll hasta aqui automaticamente.", size="2", color=rx.color("gray", 11)
                ),
                spacing="2",
                align="start",
            ),
            id="adv-footer",
            width="100%",
        ),
    )
