"""Reflex custom component wrapping react-joyride (https://react-joyride.com).

The React side lives in ``joyride_tour.jsx``, a small wrapper shipped with this
package as a shared asset. It drives react-joyride v3 through its ``useJoyride``
hook so the tour's ``controls`` can be reached from Python, normalizes
``snake_case`` props, and flattens the event payload into something the Reflex
backend can receive. This module declares the Python side: props, event
triggers and the npm dependency.

Example:
    ```python
    import reflex as rx
    import reflex_react_joyride as rjr

    class State(rx.State):
        run: bool = False

        @rx.event
        def start(self):
            self.run = True

        @rx.event
        def on_tour_end(self, event: dict):
            self.run = False

    def index():
        return rx.vstack(
            rjr.joyride(
                tour_id="main",
                run=State.run,
                continuous=True,
                steps=[
                    rjr.Step(target="#logo", content="Welcome!", placement="bottom"),
                    rjr.Step(target="#cta", content="Start here.", placement="top"),
                ],
                options=rjr.TourOptions(show_progress=True, primary_color="#7c3aed"),
                on_tour_end=State.on_tour_end,
            ),
            rx.heading("Reflex", id="logo"),
            rx.button("Get started", id="cta"),
            rx.button("Take the tour", on_click=State.start),
        )
    ```
"""

from __future__ import annotations

import re
from collections.abc import Callable
from typing import Any

import reflex as rx
from reflex.components.component import Component, NoSSRComponent
from reflex.event import passthrough_event_spec
from reflex.vars.base import Var
from reflex.vars.function import ArgsFunctionOperation

from .constants import JOYRIDE_VERSION
from .events import JoyrideEvent
from .props import FloatingOptions, Locale, Step, TourOptions, TourStyles

_JSX_ASSET = rx.asset("joyride_tour.jsx", shared=True)

# Step keys whose value is a React node and must survive normalization untouched.
_NODE_KEYS = ("content", "title")

_SNAKE_PART = re.compile(r"_+([a-zA-Z0-9])")


def _camel_key(key: Any) -> Any:
    """``spotlight_padding`` -> ``spotlightPadding``; leave ``_hover`` and ``--var`` alone."""
    if not isinstance(key, str) or key.startswith(("_", "-")) or "_" not in key:
        return key
    return _SNAKE_PART.sub(lambda match: match.group(1).upper(), key)


def _to_js_value(value: Any) -> Any:
    """Turn Reflex components into Vars so they can live inside a prop object."""
    if isinstance(value, Component):
        return Var.create(value)
    if isinstance(value, (list, tuple)):
        return [_to_js_value(item) for item in value]
    return value


def _normalize(value: Any, raw_keys: tuple[str, ...] = ()) -> Any:
    """Recursively camelCase the keys of props objects and dicts.

    ``None`` values are dropped, Reflex components become Vars, and the values
    of ``raw_keys`` (user payloads such as ``Step.data``) are copied verbatim.
    """
    if value is None or isinstance(value, Var):
        return value

    if isinstance(value, rx.PropsBase):
        value = {name: getattr(value, name, None) for name in value.get_fields()}

    if isinstance(value, dict):
        return {
            _camel_key(key): (_to_js_value(item) if key in raw_keys else _normalize(item))
            for key, item in value.items()
            if item is not None
        }

    if isinstance(value, (list, tuple)):
        return [_normalize(item) for item in value]

    return _to_js_value(value)


def _normalize_steps(steps: Any) -> Any:
    """Accept Step objects, plain dicts, or a Var, and return what JS expects."""
    if steps is None or isinstance(steps, Var):
        return steps
    if isinstance(steps, (Step, dict)):
        steps = [steps]
    return [_normalize(step, raw_keys=("data", *_NODE_KEYS)) for step in steps]


def _render_prop(name: str, fn: Callable[[Any], Component]) -> Var:
    """Turn ``lambda props: rx.box(...)`` into a React function component."""
    argument = Var(name).to(dict)
    return ArgsFunctionOperation.create((name,), Var.create(fn(argument)))


class Joyride(NoSSRComponent):
    """A react-joyride guided tour.

    The component renders nothing of its own: it mounts the tour's overlay,
    beacon and tooltip in a portal, so it can be placed anywhere on the page.
    """

    library = _JSX_ASSET.importable_path

    tag = "JoyrideTour"

    lib_dependencies: list[str] = [f"react-joyride@{JOYRIDE_VERSION}"]

    # ------------------------------------------------------------------ content
    # An id for this tour. Required to drive it from Python with the helpers in
    # ``reflex_react_joyride.actions`` (start, next_step, go_to, ...).
    tour_id: Var[str]

    # The steps of the tour: Step objects, plain dicts, or a State var holding
    # a list of dicts. ``snake_case`` keys are converted for you.
    steps: Var[list[dict[str, Any]]]

    # ----------------------------------------------------------------- playback
    # Run (or stop) the tour. Default: False.
    run: Var[bool]

    # Play the steps sequentially with a Next button instead of showing a beacon
    # between them. Default: False.
    continuous: Var[bool]

    # The step to start an uncontrolled tour at. Ignored in controlled mode.
    initial_step_index: Var[int]

    # Setting this puts the tour in *controlled* mode: react-joyride stops
    # advancing on its own and shows exactly this step, so you keep the index in
    # your State and update it from the events.
    step_index: Var[int]

    # Also scroll the page for the first step. Default: False.
    scroll_to_first_step: Var[bool]

    # Log react-joyride's internal actions to the browser console. Default: False.
    debug: Var[bool]

    # ------------------------------------------------------------- presentation
    # Behaviour and theming shared by every step (a TourOptions or a dict).
    options: Var[dict[str, Any]]

    # The strings used in the tooltip (a Locale or a dict).
    locale: Var[dict[str, Any]]

    # CSS overrides for every element react-joyride renders (a TourStyles or a dict).
    styles: Var[dict[str, Any]]

    # Positioning options forwarded to floating-ui (a FloatingOptions or a dict).
    floating_options: Var[dict[str, Any]]

    # Render the tour inside this element instead of the document body.
    portal_element: Var[str]

    # A nonce for the inline styles, for pages with a strict CSP.
    nonce: Var[str]

    # ------------------------------------------------------------- render props
    # ``lambda props: rx.card(...)`` replacing the built-in tooltip. ``props``
    # exposes react-joyride's own tooltip props (``index``, ``size``, ``step``,
    # ``isLastStep``, ...) plus ``content``, ``title``, ``current``, ``total``,
    # ``progress``, ``stepId``, ``stepData`` and ``isFirstStep``.
    tooltip: Var[Callable]

    # ``lambda props: rx.box(...)`` replacing the built-in beacon.
    beacon: Var[Callable]

    # ------------------------------------------------------------------- events
    # Fired for every react-joyride event. The payload is a JoyrideEvent dict.
    on_event: rx.EventHandler[passthrough_event_spec(JoyrideEvent)]

    # Fired once when the tour starts.
    on_tour_start: rx.EventHandler[passthrough_event_spec(JoyrideEvent)]

    # Fired when the tour finishes or is skipped. Check ``event["status"]``.
    on_tour_end: rx.EventHandler[passthrough_event_spec(JoyrideEvent)]

    # Fired whenever the tour's status changes (running, paused, finished, ...).
    on_status_change: rx.EventHandler[passthrough_event_spec(JoyrideEvent)]

    # Fired before a step is shown. In controlled mode this is usually where the
    # index moves forward.
    on_step_before: rx.EventHandler[passthrough_event_spec(JoyrideEvent)]

    # Fired after a step is closed, with the action that closed it.
    on_step_after: rx.EventHandler[passthrough_event_spec(JoyrideEvent)]

    # Fired when a step's beacon is rendered.
    on_beacon: rx.EventHandler[passthrough_event_spec(JoyrideEvent)]

    # Fired when a step's tooltip is rendered.
    on_tooltip: rx.EventHandler[passthrough_event_spec(JoyrideEvent)]

    # Fired when the page starts scrolling to a target.
    on_scroll_start: rx.EventHandler[passthrough_event_spec(JoyrideEvent)]

    # Fired when the page finished scrolling to a target.
    on_scroll_end: rx.EventHandler[passthrough_event_spec(JoyrideEvent)]

    # Fired when a step's target never appeared (see ``target_wait_timeout``).
    on_target_not_found: rx.EventHandler[passthrough_event_spec(JoyrideEvent)]

    # Fired when a step fails, e.g. a ``before`` hook rejected. Read ``event["error"]``.
    on_error: rx.EventHandler[passthrough_event_spec(JoyrideEvent)]

    @classmethod
    def create(cls, *children, **props) -> rx.Component:
        """Create a Joyride tour.

        Args:
            *children: Optionally, the steps of the tour, passed positionally.
            **props: Component props.

        Returns:
            The component.

        Raises:
            TypeError: If a render prop is neither a callable nor a Var.
        """
        if children and "steps" not in props:
            props["steps"] = list(children)
            children = ()

        props["steps"] = _normalize_steps(props.get("steps"))
        for key in ("options", "locale", "styles", "floating_options"):
            if key in props:
                props[key] = _normalize(props[key])

        for key in ("tooltip", "beacon"):
            value = props.get(key)
            if value is None or isinstance(value, Var):
                continue
            if not callable(value):
                msg = f"`{key}` must be a callable taking the render props, got {type(value).__name__}"
                raise TypeError(msg)
            props[key] = _render_prop(f"{key}Props", value)

        return super().create(*children, **props)


joyride = Joyride.create

__all__ = [
    "FloatingOptions",
    "Joyride",
    "Locale",
    "Step",
    "TourOptions",
    "TourStyles",
    "joyride",
]
