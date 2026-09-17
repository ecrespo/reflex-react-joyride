"""The constants must mirror react-joyride's literals exactly."""

import reflex_react_joyride as rjr


def test_event_values_match_react_joyride():
    assert rjr.EVENTS.TOUR_START == "tour:start"
    assert rjr.EVENTS.STEP_AFTER == "step:after"
    assert rjr.EVENTS.TARGET_NOT_FOUND == "error:target_not_found"


def test_status_and_actions():
    assert rjr.STATUS.FINISHED == "finished"
    assert rjr.STATUS.SKIPPED == "skipped"
    assert rjr.FINISHED_STATUSES == ("finished", "skipped")
    assert rjr.ACTIONS.PREV == "prev"


def test_lifecycle_and_origin():
    assert rjr.LIFECYCLE.TOOLTIP == "tooltip"
    assert rjr.ORIGIN.BUTTON_PRIMARY == "button_primary"


def test_placements_cover_auto_and_center():
    assert "auto" in rjr.PLACEMENTS
    assert "center" in rjr.PLACEMENTS
    assert "bottom-start" in rjr.PLACEMENTS
    assert rjr.PORTAL_ELEMENT_ID == "react-joyride-portal"
