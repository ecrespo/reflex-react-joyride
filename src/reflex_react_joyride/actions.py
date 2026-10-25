"""Drive a running tour from Python.

Every ``joyride(...)`` created with a ``tour_id`` registers react-joyride's
``controls`` object in the browser under ``window.__reflexJoyride[tour_id]``.
The helpers below return ``rx.call_script`` events, so they can be used as
triggers directly or returned from an event handler::

    rx.button("Start the tour", on_click=rjr.start("main"))
    rx.button("Next", on_click=rjr.next_step("main"))

They work whether the tour runs uncontrolled or in controlled mode, and they are
no-ops (with a console warning) if no tour with that id is mounted.
"""

from __future__ import annotations

import json
from typing import Any

import reflex as rx
from reflex.event import EventSpec


def _call(tour_id: str, method: str, *args: Any, callback: Any = None) -> EventSpec:
    """Call a method of the controls object registered under ``tour_id``."""
    js_args = ", ".join(json.dumps(arg) for arg in args)
    script = (
        f"(() => {{ const api = window.__reflexJoyride?.[{json.dumps(tour_id)}];"
        f" if (!api) {{ console.warn('reflex-react-joyride: no tour with id', {json.dumps(tour_id)}); return null; }}"
        f" return api.{method}({js_args}); }})()"
    )
    if callback is not None:
        return rx.call_script(script, callback=callback)
    return rx.call_script(script)


def start(tour_id: str, index: int | None = None) -> EventSpec:
    """Start (or restart) the tour, optionally at a given step index."""
    return _call(tour_id, "start") if index is None else _call(tour_id, "start", index)


def stop(tour_id: str, advance: bool = False) -> EventSpec:
    """Stop the tour. With ``advance=True`` it moves to the next step first."""
    return _call(tour_id, "stop", advance)


def next_step(tour_id: str) -> EventSpec:
    """Advance to the next step."""
    return _call(tour_id, "next")


def prev_step(tour_id: str) -> EventSpec:
    """Go back to the previous step."""
    return _call(tour_id, "prev")


def go_to(tour_id: str, index: int) -> EventSpec:
    """Jump to a specific step index (zero-based)."""
    return _call(tour_id, "go", index)


def close(tour_id: str) -> EventSpec:
    """Close the current step, advancing to the next one."""
    return _call(tour_id, "close")


def skip(tour_id: str) -> EventSpec:
    """End the tour, marking it as skipped."""
    return _call(tour_id, "skip")


def reset(tour_id: str, restart: bool = False) -> EventSpec:
    """Reset the tour to the first step; ``restart=True`` also starts it again."""
    return _call(tour_id, "reset", restart)


def replay(tour_id: str) -> EventSpec:
    """Replay the current step, re-running its hooks and events."""
    return _call(tour_id, "replay")


def open_tooltip(tour_id: str) -> EventSpec:
    """Open the tooltip of the current step (skipping its beacon)."""
    return _call(tour_id, "open")


def get_state(tour_id: str, callback: Any) -> EventSpec:
    """Send the current tour state to ``callback``, an event handler taking a dict."""
    return _call(tour_id, "info", callback=callback)


__all__ = [
    "close",
    "get_state",
    "go_to",
    "next_step",
    "open_tooltip",
    "prev_step",
    "replay",
    "reset",
    "skip",
    "start",
    "stop",
]
