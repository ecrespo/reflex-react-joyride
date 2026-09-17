"""The props objects must serialize to exactly what react-joyride expects."""

import reflex_react_joyride as rjr


def test_step_camel_cases_keys_and_drops_unset_fields():
    data = rjr.Step(target="#a", content="hi", show_progress=True, spotlight_padding=8).dict()
    assert data == {
        "target": "#a",
        "content": "hi",
        "showProgress": True,
        "spotlightPadding": 8,
    }


def test_step_inherits_every_tour_option():
    option_fields = set(rjr.TourOptions.get_fields())
    assert option_fields <= set(rjr.Step.get_fields())
    assert "z_index" in option_fields


def test_tour_options_serialize_known_keys():
    data = rjr.TourOptions(
        primary_color="#7c3aed",
        z_index=1000,
        buttons=["back", "primary"],
        dismiss_key_action=False,
        block_target_interaction=True,
    ).dict()
    assert data == {
        "primaryColor": "#7c3aed",
        "zIndex": 1000,
        "buttons": ["back", "primary"],
        "dismissKeyAction": False,
        "blockTargetInteraction": True,
    }


def test_locale_supports_the_progress_placeholder():
    assert rjr.Locale(next_with_progress="Siguiente ({current} de {total})").dict() == {
        "nextWithProgress": "Siguiente ({current} de {total})"
    }


def test_styles_convert_nested_css_properties():
    data = rjr.TourStyles(
        tooltip={"border_radius": "12px"},
        button_primary={"background_color": "#000", "fontWeight": "600"},
    ).dict()
    assert data == {
        "tooltip": {"borderRadius": "12px"},
        "buttonPrimary": {"backgroundColor": "#000", "fontWeight": "600"},
    }


def test_floating_options_accept_false_to_disable_flipping():
    assert rjr.FloatingOptions(flip_options=False, hide_arrow=True).dict() == {
        "flipOptions": False,
        "hideArrow": True,
    }


def test_spotlight_padding_per_side():
    assert rjr.SpotlightPadding(top=4, bottom=12).dict() == {"top": 4, "bottom": 12}
