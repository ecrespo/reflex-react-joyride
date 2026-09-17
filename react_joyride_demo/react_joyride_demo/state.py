"""State shared by every page of the demo: a live log of tour events."""

from __future__ import annotations

import reflex as rx
import reflex_react_joyride as rjr

#: A short label for each event type, so the log reads like a story.
EVENT_LABELS: dict[str, str] = {
    rjr.EVENTS.TOUR_START: "tour iniciado",
    rjr.EVENTS.TOUR_END: "tour terminado",
    rjr.EVENTS.TOUR_STATUS: "cambio de estado",
    rjr.EVENTS.STEP_BEFORE: "paso por mostrarse",
    rjr.EVENTS.STEP_AFTER: "paso cerrado",
    rjr.EVENTS.BEACON: "beacon visible",
    rjr.EVENTS.TOOLTIP: "tooltip visible",
    rjr.EVENTS.SCROLL_START: "scroll iniciado",
    rjr.EVENTS.SCROLL_END: "scroll terminado",
    rjr.EVENTS.TARGET_NOT_FOUND: "target no encontrado",
    rjr.EVENTS.ERROR: "error",
}


class LogState(rx.State):
    """Keeps the last events emitted by any tour on the page."""

    log: list[str] = []

    @rx.event
    def record(self, event: rjr.JoyrideEvent):
        """Append one line per event, newest first."""
        label = EVENT_LABELS.get(event["type"], event["type"])
        where = f"paso {event['index'] + 1}/{event['size']}"
        origin = f" desde {event['origin']}" if event["origin"] else ""
        self.log = [f"{event['type']} · {label} · {where} · action={event['action']}{origin}", *self.log[:11]]

    @rx.event
    def clear(self):
        """Empty the log."""
        self.log = []
