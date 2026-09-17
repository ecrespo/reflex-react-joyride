"""The component must compile to the JSX react-joyride understands."""

import pytest
import reflex as rx
import reflex_react_joyride as rjr


class DemoState(rx.State):
    run: bool = False
    index: int = 0
    steps: list[dict] = [{"target": "#a", "content": "hi"}]

    @rx.event
    def on_tour_event(self, event: dict):
        pass


def test_library_points_to_the_shared_jsx_wrapper():
    assert rjr.Joyride.library.startswith("$/public/external/reflex_react_joyride/")
    assert rjr.Joyride.library.endswith("joyride_tour.jsx")
    assert rjr.Joyride.tag == "JoyrideTour"


def test_react_joyride_is_pinned():
    assert rjr.JOYRIDE_VERSION == "3.2.0"
    assert rjr.Joyride.create(steps=[]).lib_dependencies == [f"react-joyride@{rjr.JOYRIDE_VERSION}"]


def test_steps_are_normalized_from_step_objects_and_dicts():
    rendered = str(
        rjr.joyride(
            steps=[
                rjr.Step(target="#a", content="A", spotlight_padding=8),
                {"target": "#b", "content": "B", "show_progress": True},
            ]
        )
    )
    assert '"spotlightPadding"' in rendered
    assert '"showProgress"' in rendered
    assert "spotlight_padding" not in rendered
    assert "show_progress" not in rendered


def test_step_data_keys_are_left_alone():
    rendered = str(rjr.joyride(steps=[rjr.Step(target="#a", data={"user_id": 7})]))
    assert '"user_id"' in rendered
    assert "userId" not in rendered


def test_steps_can_be_passed_positionally():
    positional = str(rjr.joyride(rjr.Step(target="#a", content="A")))
    keyword = str(rjr.joyride(steps=[rjr.Step(target="#a", content="A")]))
    assert positional == keyword


def test_step_content_accepts_reflex_components():
    rendered = str(rjr.joyride(steps=[rjr.Step(target="#a", title=rx.heading("T"), content=rx.text("C"))]))
    assert "RadixThemesHeading" in rendered
    assert "RadixThemesText" in rendered


def test_state_vars_are_passed_through_untouched():
    rendered = str(rjr.joyride(steps=DemoState.steps, run=DemoState.run, step_index=DemoState.index))
    assert "steps:" in rendered
    assert "stepIndex:" in rendered


def test_options_locale_styles_are_camel_cased():
    rendered = str(
        rjr.joyride(
            steps=[],
            options={"show_progress": True, "z_index": 1000},
            locale={"next_with_progress": "Siguiente ({current} de {total})"},
            styles={"tooltip": {"border_radius": "12px"}},
            floating_options={"hide_arrow": True},
        )
    )
    for expected in ("showProgress", "zIndex", "nextWithProgress", "borderRadius", "hideArrow"):
        assert expected in rendered


def test_every_event_trigger_is_wired():
    triggers = [
        "on_event",
        "on_tour_start",
        "on_tour_end",
        "on_status_change",
        "on_step_before",
        "on_step_after",
        "on_beacon",
        "on_tooltip",
        "on_scroll_start",
        "on_scroll_end",
        "on_target_not_found",
        "on_error",
    ]
    component = rjr.joyride(steps=[], **dict.fromkeys(triggers, DemoState.on_tour_event))
    rendered = str(component)
    for name in triggers:
        camel = "on" + "".join(part.capitalize() for part in name.split("_")[1:])
        assert f"{camel}:" in rendered, f"{name} did not render as {camel}"


def test_tooltip_render_prop_becomes_a_function_component():
    rendered = str(rjr.joyride(steps=[], tooltip=lambda props: rx.box(props["title"])))
    assert "tooltip:((tooltipProps)" in rendered.replace(" ", "")


def test_beacon_render_prop_becomes_a_function_component():
    rendered = str(rjr.joyride(steps=[], beacon=lambda props: rx.box("!")))
    assert "beacon:((beaconProps)" in rendered.replace(" ", "")


def test_render_props_must_be_callable():
    with pytest.raises(TypeError, match="must be a callable"):
        rjr.joyride(steps=[], tooltip=rx.box("not a callable"))


def test_portal_element_and_tour_id_reach_the_wrapper():
    rendered = str(rjr.joyride(steps=[], tour_id="main", portal_element="#tour-root"))
    assert "tourId:" in rendered
    assert "portalElement:" in rendered
