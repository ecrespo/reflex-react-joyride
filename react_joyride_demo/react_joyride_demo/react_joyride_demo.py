"""reflex-react-joyride demo app.

Four pages, each one a tour: the basics, controlled mode, theming with a custom
tooltip, and the awkward cases (missing targets, scrolling, modal steps).

    cd react_joyride_demo && uv run reflex run
"""

from __future__ import annotations

import reflex as rx

from . import pages  # noqa: F401  - importing the modules registers their @rx.page

# The Radix theme is configured through RadixThemesPlugin in rxconfig.py.
app = rx.App(
    style={"font_family": "Inter, ui-sans-serif, system-ui, sans-serif"},
)
