"""Page 3 - locale, theming and a tooltip written in Reflex.

Three things at once:

* ``locale`` translates every button of the built-in tooltip.
* ``options`` and ``styles`` restyle it without leaving Python. Here they come
  from a computed var, which proves that ``snake_case`` keys are normalized at
  runtime too, not only when the props are literals.
* ``tooltip=lambda props: ...`` replaces the tooltip altogether with an ordinary
  Reflex component, wired to the tour with the imperative helpers.
"""

from __future__ import annotations

import reflex as rx
import reflex_react_joyride as rjr

from ..layout import shell
from ..state import LogState

TOUR_ID = "tema"

PALETTES = {
    "violeta": {"primary": "#7c3aed", "overlay": "rgba(24, 12, 48, 0.55)", "surface": "#faf7ff"},
    "esmeralda": {"primary": "#059669", "overlay": "rgba(4, 47, 36, 0.55)", "surface": "#f2fbf7"},
    "ambar": {"primary": "#d97706", "overlay": "rgba(69, 39, 3, 0.55)", "surface": "#fffaf0"},
}

STEPS = [
    rjr.Step(
        target="#theme-palette",
        title="Paleta",
        content="Cambia la paleta desde el dock sin cerrar el tour: options y styles salen de un computed var.",
        placement="bottom",
    ),
    rjr.Step(
        target="#theme-locale",
        title="Textos",
        content="Los botones del tooltip integrado estan traducidos con locale.",
        placement="right",
    ),
    rjr.Step(
        target="#theme-custom",
        title="Tooltip propio",
        content="El interruptor del dock sustituye el tooltip integrado por este componente Reflex.",
        placement="left",
    ),
]

SPANISH = rjr.Locale(
    back="Atras",
    close="Cerrar",
    last="Finalizar",
    next="Siguiente",
    next_with_progress="Siguiente ({current} de {total})",
    open="Abrir la guia",
    skip="Saltar",
)


class ThemeState(rx.State):
    """Palette, locale and custom-tooltip switches for this page."""

    run: bool = False
    palette: str = "violeta"
    custom_tooltip: bool = False

    @rx.var
    def primary(self) -> str:
        """The active palette's primary color, also used by the custom tooltip."""
        return PALETTES[self.palette]["primary"]

    @rx.var
    def tour_options(self) -> dict:
        """Options built in Python, with snake_case keys the wrapper normalizes."""
        colors = PALETTES[self.palette]
        return {
            "primary_color": colors["primary"],
            "background_color": colors["surface"],
            "arrow_color": colors["surface"],
            "overlay_color": colors["overlay"],
            "text_color": "#1f2937",
            "show_progress": True,
            "skip_beacon": True,
            "spotlight_radius": 12,
            "spotlight_padding": 10,
            "buttons": ["back", "skip", "primary"],
            "z_index": 1000,
            "width": 420,
        }

    @rx.var
    def tour_styles(self) -> dict:
        """Style overrides; the CSS keys are snake_case here as well."""
        colors = PALETTES[self.palette]
        return {
            "tooltip": {"border_radius": "14px", "box_shadow": "0 18px 40px rgba(15, 23, 42, 0.18)"},
            "tooltip_title": {"font_size": "18px", "font_weight": "700", "color": colors["primary"]},
            "tooltip_content": {"padding": "12px 4px", "line_height": "1.6"},
            "button_primary": {"border_radius": "999px", "padding": "8px 18px", "font_weight": "600"},
            "button_back": {"color": colors["primary"], "font_weight": "600"},
            "button_skip": {"color": "#9ca3af"},
        }

    @rx.event
    def start(self):
        self.run = True

    @rx.event
    def finish(self, _event: rjr.JoyrideEvent):
        self.run = False

    @rx.event
    def set_palette(self, palette: str | list[str]):
        self.palette = palette if isinstance(palette, str) else palette[0]

    @rx.event
    def toggle_custom(self, value: bool):
        self.custom_tooltip = value


def custom_tooltip(props: rx.Var) -> rx.Component:
    """A tooltip rendered entirely with Reflex components.

    ``props`` carries what react-joyride passes to a custom tooltip plus a few
    conveniences added by the wrapper: ``current``, ``total``, ``progress``,
    ``content``, ``title``, ``stepId``, ``stepData``, ``isFirstStep`` and
    ``isLastStep``.
    """
    return rx.card(
        rx.vstack(
            rx.hstack(
                rx.badge(props["progress"], variant="solid", radius="full", background=ThemeState.primary),
                rx.spacer(),
                rx.icon_button(
                    rx.icon("x", size=14),
                    size="1",
                    variant="ghost",
                    color_scheme="gray",
                    on_click=rjr.skip(TOUR_ID),
                ),
                width="100%",
                align="center",
            ),
            rx.heading(props["title"], size="4"),
            rx.text(props["content"], size="2", color=rx.color("gray", 11)),
            rx.hstack(
                rx.button(
                    "Atras",
                    size="2",
                    variant="soft",
                    on_click=rjr.prev_step(TOUR_ID),
                    disabled=props["isFirstStep"].to(bool),
                ),
                rx.spacer(),
                rx.button(
                    rx.cond(props["isLastStep"].to(bool), "Finalizar", "Siguiente"),
                    size="2",
                    background=ThemeState.primary,
                    on_click=rjr.next_step(TOUR_ID),
                ),
                width="100%",
                align="center",
            ),
            spacing="3",
            align="start",
            width="100%",
        ),
        width="360px",
        background=rx.color("gray", 1),
    )


def custom_beacon(_props: rx.Var) -> rx.Component:
    """A beacon rendered with Reflex instead of the built-in pulsing dot."""
    return rx.box(
        rx.icon("sparkles", size=16, color="white"),
        display="flex",
        align_items="center",
        justify_content="center",
        width="34px",
        height="34px",
        border_radius="999px",
        background=ThemeState.primary,
        box_shadow="0 0 0 6px rgba(124, 58, 237, 0.25)",
        cursor="pointer",
    )


def palette_swatch(name: str) -> rx.Component:
    """One clickable-looking swatch; the real control lives in the dock."""
    colors = PALETTES[name]
    return rx.hstack(
        rx.box(width="18px", height="18px", border_radius="6px", background=colors["primary"]),
        rx.text(name.capitalize(), size="2"),
        rx.cond(
            ThemeState.palette == name,
            rx.badge("activa", color_scheme="violet", size="1"),
            rx.fragment(),
        ),
        spacing="2",
        align="center",
    )


@rx.page(route="/tema", title="reflex-react-joyride - tema y locale")
def theming_page() -> rx.Component:
    """Locale in Spanish, themed options and an optional Reflex tooltip."""
    return shell(
        "Tema y locale",
        "El mismo tour con textos en espanol, estilos propios y un tooltip hecho con Reflex.",
        [
            rx.button(
                rx.icon("play", size=16), "Iniciar tour", on_click=ThemeState.start, disabled=ThemeState.run
            ),
            rx.button(
                "Reiniciar",
                variant="soft",
                on_click=rjr.reset(TOUR_ID, restart=True),
                disabled=~ThemeState.run,
            ),
            rx.segmented_control.root(
                rx.segmented_control.item("Violeta", value="violeta"),
                rx.segmented_control.item("Esmeralda", value="esmeralda"),
                rx.segmented_control.item("Ambar", value="ambar"),
                value=ThemeState.palette,
                on_change=ThemeState.set_palette,
                size="1",
            ),
            rx.hstack(
                rx.switch(checked=ThemeState.custom_tooltip, on_change=ThemeState.toggle_custom, size="1"),
                rx.text("Tooltip Reflex", size="1"),
                spacing="2",
                align="center",
            ),
        ],
        rx.cond(
            ThemeState.custom_tooltip,
            rjr.joyride(
                tour_id=TOUR_ID,
                steps=STEPS,
                portal_element="#tour-root",
                run=ThemeState.run,
                continuous=True,
                options=ThemeState.tour_options,
                locale=SPANISH,
                styles=ThemeState.tour_styles,
                tooltip=custom_tooltip,
                beacon=custom_beacon,
                on_event=LogState.record,
                on_tour_end=ThemeState.finish,
            ),
            rjr.joyride(
                tour_id=TOUR_ID,
                steps=STEPS,
                portal_element="#tour-root",
                run=ThemeState.run,
                continuous=True,
                options=ThemeState.tour_options,
                locale=SPANISH,
                styles=ThemeState.tour_styles,
                on_event=LogState.record,
                on_tour_end=ThemeState.finish,
            ),
        ),
        rx.grid(
            rx.card(
                rx.vstack(
                    rx.heading("Paleta", size="3"),
                    rx.text(
                        "Cambiala desde el dock, incluso con el tour abierto.",
                        size="1",
                        color=rx.color("gray", 11),
                    ),
                    palette_swatch("violeta"),
                    palette_swatch("esmeralda"),
                    palette_swatch("ambar"),
                    spacing="2",
                    align="start",
                ),
                id="theme-palette",
            ),
            rx.card(
                rx.vstack(
                    rx.heading("Locale", size="3"),
                    rx.text(
                        "Atras · Saltar · Siguiente (1 de 3) · Finalizar",
                        size="2",
                        color=rx.color("gray", 11),
                    ),
                    rx.text(
                        "Cada cadena del tooltip integrado sale de rjr.Locale.",
                        size="1",
                        color=rx.color("gray", 10),
                    ),
                    spacing="2",
                    align="start",
                ),
                id="theme-locale",
            ),
            rx.card(
                rx.vstack(
                    rx.heading("Tooltip propio", size="3"),
                    rx.cond(
                        ThemeState.custom_tooltip,
                        rx.badge("Componente Reflex", color_scheme="violet", size="2"),
                        rx.badge("Tooltip integrado", color_scheme="gray", size="2"),
                    ),
                    rx.text(
                        "El interruptor del dock cambia entre los dos.", size="1", color=rx.color("gray", 11)
                    ),
                    spacing="2",
                    align="start",
                ),
                id="theme-custom",
            ),
            columns="3",
            spacing="4",
            width="100%",
        ),
    )
