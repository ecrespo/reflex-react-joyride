"""The action helpers must target the right tour and method."""

import reflex_react_joyride as rjr
from reflex_react_joyride import actions


def script_of(event_spec) -> str:
    """The JS snippet an action helper compiles to, with the Var quoting undone."""
    return str(event_spec.args[0][1]).replace('\\"', '"')


def test_every_action_is_exported():
    for name in (
        "start",
        "stop",
        "next_step",
        "prev_step",
        "go_to",
        "close",
        "skip",
        "reset",
        "replay",
        "open_tooltip",
        "get_state",
    ):
        assert hasattr(rjr, name), name
        assert hasattr(actions, name), name


def test_actions_call_the_registry_entry_for_the_tour():
    script = script_of(rjr.next_step("welcome"))
    assert "window.__reflexJoyride" in script
    assert '"welcome"' in script
    assert "api.next()" in script


def test_start_can_take_an_index():
    assert "api.start()" in script_of(rjr.start("welcome"))
    assert "api.start(3)" in script_of(rjr.start("welcome", 3))


def test_go_to_passes_the_index_and_reset_the_restart_flag():
    assert "api.go(2)" in script_of(rjr.go_to("welcome", 2))
    assert "api.reset(true)" in script_of(rjr.reset("welcome", restart=True))
    assert "api.reset(false)" in script_of(rjr.reset("welcome"))


def test_missing_tour_only_warns():
    assert "console.warn" in script_of(rjr.skip("nope"))
