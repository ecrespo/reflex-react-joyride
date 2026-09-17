"""Constants mirroring the literals exported by react-joyride v3.

The values are the exact strings react-joyride emits, so they can be compared
directly against the payload received by ``on_event`` and friends::

    from reflex_react_joyride import EVENTS, STATUS

    @rx.event
    def tour_event(self, event: dict):
        if event["type"] == EVENTS.TOUR_END:
            self.finished = event["status"] == STATUS.FINISHED
"""

from __future__ import annotations

from typing import Final, Literal

#: npm version of react-joyride this component wraps.
JOYRIDE_VERSION: Final = "3.2.0"

#: The id of the portal element react-joyride renders into.
PORTAL_ELEMENT_ID: Final = "react-joyride-portal"


class ACTIONS:
    """The action that triggered a state update (``event["action"]``)."""

    INIT: Final = "init"
    START: Final = "start"
    STOP: Final = "stop"
    RESET: Final = "reset"
    PREV: Final = "prev"
    NEXT: Final = "next"
    GO: Final = "go"
    CLOSE: Final = "close"
    SKIP: Final = "skip"
    REPLAY: Final = "replay"
    UPDATE: Final = "update"
    COMPLETE: Final = "complete"


class EVENTS:
    """The type of the event (``event["type"]``)."""

    TOUR_START: Final = "tour:start"
    STEP_BEFORE_HOOK: Final = "step:before_hook"
    STEP_BEFORE: Final = "step:before"
    SCROLL_START: Final = "scroll:start"
    SCROLL_END: Final = "scroll:end"
    BEACON: Final = "beacon"
    TOOLTIP: Final = "tooltip"
    STEP_AFTER: Final = "step:after"
    STEP_AFTER_HOOK: Final = "step:after_hook"
    TOUR_END: Final = "tour:end"
    TOUR_STATUS: Final = "tour:status"
    TARGET_NOT_FOUND: Final = "error:target_not_found"
    ERROR: Final = "error"


class LIFECYCLE:
    """The rendering phase of the current step (``event["lifecycle"]``)."""

    INIT: Final = "init"
    READY: Final = "ready"
    BEACON_BEFORE: Final = "beacon_before"
    BEACON: Final = "beacon"
    TOOLTIP_BEFORE: Final = "tooltip_before"
    TOOLTIP: Final = "tooltip"
    COMPLETE: Final = "complete"


class ORIGIN:
    """The UI element that triggered the action (``event["origin"]``)."""

    BUTTON_BACK: Final = "button_back"
    BUTTON_CLOSE: Final = "button_close"
    BUTTON_PRIMARY: Final = "button_primary"
    BUTTON_SKIP: Final = "button_skip"
    KEYBOARD: Final = "keyboard"
    OVERLAY: Final = "overlay"


class STATUS:
    """The tour's current status (``event["status"]``)."""

    IDLE: Final = "idle"
    READY: Final = "ready"
    WAITING: Final = "waiting"
    RUNNING: Final = "running"
    PAUSED: Final = "paused"
    SKIPPED: Final = "skipped"
    FINISHED: Final = "finished"


#: Statuses that mean the tour is over, one way or another.
FINISHED_STATUSES: Final = (STATUS.FINISHED, STATUS.SKIPPED)

ActionType = Literal[
    "init", "start", "stop", "reset", "prev", "next", "go", "close", "skip", "replay", "update", "complete"
]
EventType = Literal[
    "tour:start",
    "step:before_hook",
    "step:before",
    "scroll:start",
    "scroll:end",
    "beacon",
    "tooltip",
    "step:after",
    "step:after_hook",
    "tour:end",
    "tour:status",
    "error:target_not_found",
    "error",
]
LifecycleType = Literal["init", "ready", "beacon_before", "beacon", "tooltip_before", "tooltip", "complete"]
OriginType = Literal["button_back", "button_close", "button_primary", "button_skip", "keyboard", "overlay"]
StatusType = Literal["idle", "ready", "waiting", "running", "paused", "skipped", "finished"]

#: Placements accepted by the beacon and the tooltip.
Placement = Literal[
    "top",
    "top-start",
    "top-end",
    "bottom",
    "bottom-start",
    "bottom-end",
    "left",
    "left-start",
    "left-end",
    "right",
    "right-start",
    "right-end",
]

#: ``placement`` also accepts ``auto`` (let floating-ui decide) and ``center``
#: (a modal-like step with no arrow, useful for a welcome step).
StepPlacement = Literal[
    "top",
    "top-start",
    "top-end",
    "bottom",
    "bottom-start",
    "bottom-end",
    "left",
    "left-start",
    "left-end",
    "right",
    "right-start",
    "right-end",
    "auto",
    "center",
]

#: The buttons rendered in the tooltip footer, in order.
ButtonType = Literal["back", "close", "primary", "skip"]

#: What opens the tooltip when the beacon is shown.
BeaconTrigger = Literal["click", "hover"]

#: What the close button does.
CloseButtonAction = Literal["close", "skip", "replay"]

#: What the ESC key does (``False`` disables it).
DismissKeyAction = Literal["close", "next", "replay"]

#: What a click on the overlay does (``False`` disables it).
OverlayClickAction = Literal["close", "next", "replay"]

#: Positioning strategy used by floating-ui.
Strategy = Literal["absolute", "fixed"]

PLACEMENTS: Final = (
    "top",
    "top-start",
    "top-end",
    "bottom",
    "bottom-start",
    "bottom-end",
    "left",
    "left-start",
    "left-end",
    "right",
    "right-start",
    "right-end",
    "auto",
    "center",
)
