"""reflex-react-joyride: guided product tours for Reflex, powered by react-joyride."""

from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as _package_version

from . import actions
from .actions import (
    close,
    get_state,
    go_to,
    next_step,
    open_tooltip,
    prev_step,
    replay,
    reset,
    skip,
    start,
    stop,
)
from .constants import (
    ACTIONS,
    EVENTS,
    FINISHED_STATUSES,
    JOYRIDE_VERSION,
    LIFECYCLE,
    ORIGIN,
    PLACEMENTS,
    PORTAL_ELEMENT_ID,
    STATUS,
)
from .events import JoyrideEvent, TourState
from .joyride import Joyride, joyride
from .props import (
    FloatingOptions,
    Locale,
    SpotlightPadding,
    Step,
    TourOptions,
    TourStyles,
)

# pyproject.toml is the single source of truth for the version; read it back
# from the installed metadata so the two can never drift.
try:
    __version__ = _package_version("reflex-react-joyride")
except PackageNotFoundError:  # pragma: no cover - source tree without an install
    __version__ = "0.0.0.dev0"

__all__ = [
    "ACTIONS",
    "EVENTS",
    "FINISHED_STATUSES",
    "JOYRIDE_VERSION",
    "LIFECYCLE",
    "ORIGIN",
    "PLACEMENTS",
    "PORTAL_ELEMENT_ID",
    "STATUS",
    "FloatingOptions",
    "Joyride",
    "JoyrideEvent",
    "Locale",
    "SpotlightPadding",
    "Step",
    "TourOptions",
    "TourState",
    "TourStyles",
    "actions",
    "close",
    "get_state",
    "go_to",
    "joyride",
    "next_step",
    "open_tooltip",
    "prev_step",
    "replay",
    "reset",
    "skip",
    "start",
    "stop",
]
