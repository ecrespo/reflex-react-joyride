"""The payloads delivered to the component's event triggers.

react-joyride's own ``onEvent`` callback receives the merged step object, which
carries React nodes and functions and cannot cross the wire. The JSX wrapper
therefore reduces it to the flat, JSON-safe :class:`JoyrideEvent` below, with
``snake_case`` keys so it reads naturally from Python::

    @rx.event
    def on_tour_event(self, event: rjr.JoyrideEvent):
        self.log.append(f"{event['type']} -> step {event['index'] + 1}")
"""

from __future__ import annotations

from typing import Any, TypedDict


class JoyrideEvent(TypedDict):
    """The payload of every event trigger.

    It is a plain ``dict`` at runtime, so annotate handlers with ``dict`` if you
    prefer: ``def handler(self, event: dict)``.
    """

    # The event that fired, e.g. "tour:start" or "step:after". See EVENTS.
    type: str
    # The action that triggered it, e.g. "next", "prev", "close". See ACTIONS.
    action: str
    # The index of the current step, zero-based.
    index: int
    # The total number of steps.
    size: int
    # The tour status: idle, ready, waiting, running, paused, skipped, finished.
    status: str
    # The step's rendering phase: init, ready, beacon, tooltip, complete, ...
    lifecycle: str
    # Which control triggered the action ("button_primary", "overlay", ...), or None.
    origin: str | None
    # Whether the tour is running in controlled mode (``step_index`` is set).
    controlled: bool
    # Whether the tour is waiting for a target to appear or a hook to resolve.
    waiting: bool
    # Whether the page is being scrolled to the target right now.
    scrolling: bool
    # ``index == size - 1``.
    is_last_step: bool
    # The current step's ``id``, if it has one.
    step_id: str | None
    # The current step's ``target`` when it is a CSS selector.
    step_target: str | None
    # The current step's ``title`` when it is a plain string.
    step_title: str | None
    # The current step's ``data``, passed through untouched.
    step_data: Any | None
    # The error message for "error" events, otherwise None.
    error: str | None


class TourState(TypedDict):
    """The tour state returned by :func:`reflex_react_joyride.actions.get_state`."""

    action: str
    controlled: bool
    index: int
    lifecycle: str
    origin: str | None
    scrolling: bool
    size: int
    status: str
    waiting: bool


__all__ = ["JoyrideEvent", "TourState"]
