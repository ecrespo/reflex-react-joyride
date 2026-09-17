"""Page 2 - controlled mode.

With ``step_index`` set, react-joyride stops advancing on its own: it renders
exactly the step you ask for. The index lives in the State, and ``on_step_after``
moves it forward or backward depending on the action that closed the step. That
is what lets the buttons outside the tooltip drive the tour, and what you need
when a step should only open after your own code did something.
"""

from __future__ import annotations

import reflex as rx
import reflex_react_joyride as rjr

from ..layout import shell
from ..state import LogState

TOUR_ID = "controlado"

STEPS = [
    rjr.Step(
        target="#ctrl-plan",
        title="1. Elige un plan",
        content="En modo controlado el paso visible es exactamente el que dice tu State.",
        placement="right",
    ),
    rjr.Step(
        target="#ctrl-seats",
        title="2. Asientos",
        content="Los botones de abajo mueven el indice sin tocar el tooltip.",
        placement="right",
    ),
    rjr.Step(
        target="#ctrl-summary",
        title="3. Resumen",
        content="Puedes saltar a cualquier paso: basta con asignar el indice.",
        placement="left",
    ),
    rjr.Step(
        target="#ctrl-confirm",
        title="4. Confirmar",
        content="Al cerrar este paso el tour emite tour:end y apagamos run.",
        placement="top",
    ),
]

PLANS = [("Starter", "19"), ("Pro", "49"), ("Scale", "129")]


class ControlledState(rx.State):
    """Owns both the run flag and the step index."""

    run: bool = False
    index: int = 0
    plan: str = "Pro"
    seats: int = 5

    @rx.var
    def total(self) -> int:
        """The fake invoice total, so the tour has something to talk about."""
        price = {"Starter": 19, "Pro": 49, "Scale": 129}[self.plan]
        return price * self.seats

    @rx.var
    def position(self) -> str:
        """A human readable position, shown next to the buttons."""
        return f"{self.index + 1} / {len(STEPS)}"

    @rx.event
    def start(self):
        """Start from the first step."""
        self.index = 0
        self.run = True

    @rx.event
    def stop(self):
        """Stop the tour without finishing it."""
        self.run = False

    @rx.event
    def advance(self, event: rjr.JoyrideEvent):
        """Move the index after a step closes, following the action that closed it."""
        self.index = max(0, event["index"] + (-1 if event["action"] == rjr.ACTIONS.PREV else 1))

    @rx.event
    def skip_missing(self, event: rjr.JoyrideEvent):
        """A target that never showed up should not block the tour."""
        self.index = event["index"] + 1

    @rx.event
    def finish(self, _event: rjr.JoyrideEvent):
        """Reset when react-joyride reports the tour is over."""
        self.run = False
        self.index = 0

    @rx.event
    def go(self, index: int):
        """Jump to a step from the buttons below."""
        self.index = min(max(index, 0), len(STEPS) - 1)
        self.run = True

    @rx.event
    def set_plan(self, plan: str):
        self.plan = plan

    @rx.event
    def set_seats(self, seats: list[int | float]):
        self.seats = int(seats[0])


@rx.page(route="/controlado", title="reflex-react-joyride - modo controlado")
def controlled_page() -> rx.Component:
    """A tour whose index is owned by the Reflex State."""
    return shell(
        "Modo controlado",
        "step_index vive en el State: el tour muestra el paso que tu decidas.",
        [
            rx.button(
                rx.icon("play", size=16),
                "Iniciar",
                on_click=ControlledState.start,
                disabled=ControlledState.run,
            ),
            rx.button(
                "Anterior",
                variant="soft",
                on_click=ControlledState.go(ControlledState.index - 1),
                disabled=~ControlledState.run,
            ),
            rx.button(
                "Siguiente",
                variant="soft",
                on_click=ControlledState.go(ControlledState.index + 1),
                disabled=~ControlledState.run,
            ),
            rx.badge(ControlledState.position, size="2", variant="surface"),
            rx.button(
                "Detener",
                variant="soft",
                color_scheme="gray",
                on_click=ControlledState.stop,
                disabled=~ControlledState.run,
            ),
        ],
        rjr.joyride(
            tour_id=TOUR_ID,
            steps=STEPS,
            portal_element="#tour-root",
            run=ControlledState.run,
            step_index=ControlledState.index,
            continuous=True,
            options=rjr.TourOptions(
                show_progress=True,
                skip_beacon=True,
                primary_color=rx.color("violet", 9),
                spotlight_padding=12,
                z_index=1000,
            ),
            on_event=LogState.record,
            on_step_after=ControlledState.advance,
            on_target_not_found=ControlledState.skip_missing,
            on_tour_end=ControlledState.finish,
        ),
        rx.grid(
            rx.card(
                rx.vstack(
                    rx.heading("Plan", size="3"),
                    rx.radio(
                        [name for name, _ in PLANS],
                        value=ControlledState.plan,
                        on_change=ControlledState.set_plan,
                        direction="column",
                        spacing="2",
                    ),
                    spacing="3",
                    align="start",
                ),
                id="ctrl-plan",
            ),
            rx.card(
                rx.vstack(
                    rx.heading("Asientos", size="3"),
                    rx.text(f"{ControlledState.seats} personas", size="2", color=rx.color("gray", 11)),
                    rx.slider(
                        default_value=[5],
                        min=1,
                        max=50,
                        on_change=ControlledState.set_seats,
                        width="100%",
                    ),
                    spacing="3",
                    align="start",
                    width="100%",
                ),
                id="ctrl-seats",
            ),
            rx.card(
                rx.vstack(
                    rx.heading("Resumen", size="3"),
                    rx.text(ControlledState.plan, size="2"),
                    rx.heading(f"${ControlledState.total} / mes", size="5"),
                    spacing="2",
                    align="start",
                ),
                id="ctrl-summary",
            ),
            columns="3",
            spacing="4",
            width="100%",
        ),
        rx.hstack(
            rx.text("Todo correcto?", size="2", color=rx.color("gray", 11)),
            rx.spacer(),
            rx.button("Confirmar suscripcion", id="ctrl-confirm"),
            width="100%",
            align="center",
        ),
    )
