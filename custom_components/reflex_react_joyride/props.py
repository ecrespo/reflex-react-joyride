"""Typed prop objects for react-joyride.

Every class here is a :class:`reflex.PropsBase`, so ``snake_case`` field names
are serialized as the ``camelCase`` keys react-joyride expects and unset fields
are dropped entirely::

    TourOptions(show_progress=True, primary_color="#7c3aed").dict()
    # {'showProgress': True, 'primaryColor': '#7c3aed'}

Plain dictionaries work too — :func:`reflex_react_joyride.joyride` converts them
into these objects, and the JSX wrapper normalizes ``snake_case`` keys again at
runtime so steps stored in a Reflex ``State`` behave the same way.
"""

from __future__ import annotations

from typing import Any

import reflex as rx

from .constants import (
    BeaconTrigger,
    ButtonType,
    CloseButtonAction,
    DismissKeyAction,
    OverlayClickAction,
    Placement,
    StepPlacement,
    Strategy,
)


class SpotlightPadding(rx.PropsBase):
    """Per-side padding around the spotlight cutout, in pixels."""

    top: int | None
    right: int | None
    bottom: int | None
    left: int | None


class Locale(rx.PropsBase):
    """The strings used in the tooltip.

    Every field also accepts a Reflex component instead of a string.
    """

    # Label for the back button. Default: "Back".
    back: Any | None
    # Label for the close button. Default: "Close".
    close: Any | None
    # Label for the primary button on the last step. Default: "Last".
    last: Any | None
    # Label for the primary button. Default: "Next".
    next: Any | None
    # Label used instead of ``next`` when ``show_progress`` is on.
    # Supports the ``{current}`` and ``{total}`` placeholders.
    # Default: "Next ({current} of {total})".
    next_with_progress: Any | None
    # Aria label of the beacon button. Default: "Open the dialog".
    open: Any | None
    # Label for the skip button. Default: "Skip".
    skip: Any | None


class TourStyles(rx.PropsBase):
    """CSS overrides for every element react-joyride renders.

    Each field is a style dict; ``snake_case`` CSS properties are converted to
    the ``camelCase`` React expects (``background_color`` -> ``backgroundColor``).
    """

    # The tooltip arrow (an SVG polygon).
    arrow: dict[str, Any] | None
    # The default beacon content.
    beacon: dict[str, Any] | None
    # The beacon's inner pulsing dot.
    beacon_inner: dict[str, Any] | None
    # The beacon's outer ring.
    beacon_outer: dict[str, Any] | None
    # The <button> wrapping the beacon.
    beacon_wrapper: dict[str, Any] | None
    # The "Back" button.
    button_back: dict[str, Any] | None
    # The "x" close button.
    button_close: dict[str, Any] | None
    # The "Next"/"Last" button.
    button_primary: dict[str, Any] | None
    # The "Skip" button.
    button_skip: dict[str, Any] | None
    # The floating container holding the tooltip.
    floater: dict[str, Any] | None
    # The loader shown while a ``before`` hook or a missing target is pending.
    loader: dict[str, Any] | None
    # The backdrop covering the page.
    overlay: dict[str, Any] | None
    # The spotlight cutout (an SVG path, so it takes SVG attributes).
    spotlight: dict[str, Any] | None
    # The tooltip itself.
    tooltip: dict[str, Any] | None
    # The tooltip's inner container.
    tooltip_container: dict[str, Any] | None
    # The tooltip's body.
    tooltip_content: dict[str, Any] | None
    # The tooltip's footer (where the buttons live).
    tooltip_footer: dict[str, Any] | None
    # The flexible spacer between the skip button and the rest.
    tooltip_footer_spacer: dict[str, Any] | None
    # The tooltip's title.
    tooltip_title: dict[str, Any] | None


class FloatingOptions(rx.PropsBase):
    """Positioning options forwarded to floating-ui."""

    # Options for floating-ui's autoUpdate (ancestorScroll, elementResize, ...).
    auto_update: dict[str, Any] | None
    # Beacon positioning, e.g. ``{"offset": 4}``.
    beacon_options: dict[str, Any] | None
    # Options for the flip middleware, or ``False`` to never flip.
    flip_options: dict[str, Any] | bool | None
    # Hide the arrow (a ``center`` placement hides it anyway). Default: False.
    hide_arrow: bool | None
    # Options for the shift middleware. Default padding: 10.
    shift_options: dict[str, Any] | None
    # "absolute" (default) or "fixed" (the default when the step is fixed).
    strategy: Strategy | None


class TourOptions(rx.PropsBase):
    """Behaviour and theming shared by every step.

    Pass it as ``joyride(options=TourOptions(...))`` for the whole tour, or set
    the same fields on an individual :class:`Step` to override them there.
    """

    # Width of the arrow's base edge, in pixels. Default: 32.
    arrow_base: int | None
    # Arrow fill color. Default: "#ffffff".
    arrow_color: str | None
    # Arrow height, tip to base, in pixels. Default: 16.
    arrow_size: int | None
    # Distance between the arrow and the tooltip edge. Default: 12.
    arrow_spacing: int | None
    # Tooltip background color. Default: "#ffffff".
    background_color: str | None
    # Beacon diameter in pixels. Default: 36.
    beacon_size: int | None
    # What opens the tooltip: "click" (default) or "hover".
    beacon_trigger: BeaconTrigger | None
    # Max milliseconds to wait for a ``before`` hook. 0 disables. Default: 5000.
    before_timeout: int | None
    # Block clicks on the highlighted element. Default: False.
    block_target_interaction: bool | None
    # Buttons shown in the footer. Default: ["back", "close", "primary"].
    buttons: list[ButtonType] | None
    # What the close button does: "close" (default), "skip" or "replay".
    close_button_action: CloseButtonAction | None
    # Let focus leave the tooltip. Default: False.
    disable_focus_trap: bool | None
    # What ESC does: "close" (default), "next", "replay", or False to disable.
    dismiss_key_action: DismissKeyAction | bool | None
    # Render the tour without the backdrop. Default: False.
    hide_overlay: bool | None
    # Delay before showing the loader while waiting, in ms. Default: 300.
    loader_delay: int | None
    # Distance between the tooltip and the spotlight, in pixels. Default: 10.
    offset: int | None
    # What a click on the overlay does: "close" (default), "next", "replay", or False.
    overlay_click_action: OverlayClickAction | bool | None
    # Backdrop color. Default: "#00000080".
    overlay_color: str | None
    # Primary button and beacon color. Default: "#000000".
    primary_color: str | None
    # Scroll animation duration in ms. Default: 300.
    scroll_duration: int | None
    # Distance from the element's scrollTop. Default: 20.
    scroll_offset: int | None
    # Show "(1 of 5)" in the primary button. Default: False.
    show_progress: bool | None
    # Show the tooltip directly, without the beacon. Default: False.
    skip_beacon: bool | None
    # Never scroll to the target. Default: False.
    skip_scroll: bool | None
    # Spotlight padding: a number, or a dict/SpotlightPadding per side. Default: 10.
    spotlight_padding: int | SpotlightPadding | dict[str, int] | None
    # Border radius of the spotlight cutout, in pixels. Default: 4.
    spotlight_radius: int | None
    # Max milliseconds to wait for a missing target. 0 disables. Default: 1000.
    target_wait_timeout: int | None
    # Tooltip text color. Default: "#000000".
    text_color: str | None
    # Tooltip width, a number of pixels or any CSS length. Default: 380.
    width: str | int | None
    # z-index of the overlay and the tooltip. Default: 100.
    z_index: int | None


class Step(TourOptions):
    """A single step of the tour.

    ``target`` is the only required field. Everything :class:`TourOptions`
    offers can be overridden here for this step alone::

        Step(
            target="#sidebar",
            title="Navigation",
            content="Every section of the app lives here.",
            placement="right",
            show_progress=True,
        )
    """

    # A CSS selector for the element the step points at. ``"body"`` with
    # ``placement="center"`` gives a modal-like step.
    target: Any | None
    # The tooltip body: a string, or any Reflex component.
    content: Any | None
    # The tooltip title: a string, or any Reflex component.
    title: Any | None
    # A stable identifier, echoed back as ``step_id`` in every event.
    id: str | None
    # Arbitrary data echoed back as ``step_data`` in every event. Keys are
    # passed through untouched.
    data: Any | None
    # Keep the step fixed while the page scrolls. Default: False.
    is_fixed: bool | None
    # Where the tooltip sits relative to the target. Default: "bottom".
    placement: StepPlacement | None
    # Where the beacon sits; defaults to ``placement``.
    beacon_placement: Placement | None
    # Scroll to this element instead of ``target``.
    scroll_target: Any | None
    # Highlight this element instead of ``target``; the tooltip still anchors
    # to ``target``.
    spotlight_target: Any | None
    # Tooltip strings for this step only.
    locale: Locale | dict[str, Any] | None
    # Style overrides for this step only.
    styles: TourStyles | dict[str, Any] | None
    # floating-ui options for this step only.
    floating_options: FloatingOptions | dict[str, Any] | None


__all__ = [
    "FloatingOptions",
    "Locale",
    "SpotlightPadding",
    "Step",
    "TourOptions",
    "TourStyles",
]
