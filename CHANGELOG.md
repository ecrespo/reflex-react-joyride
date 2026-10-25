# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses
[Semantic Versioning](https://semver.org/).

## [0.3.0] - 2026-10-25

### Changed

- Migrated to the layout of Reflex's official
  [component template](https://github.com/reflex-dev/component-template):
  - the package moved from `custom_components/` to `src/reflex_react_joyride/`
    and the demo app from `react_joyride_demo/` to `demo/`;
  - builds with hatchling instead of setuptools;
  - the version comes from the git tag (`uv-dynamic-versioning`) and is no
    longer written in `pyproject.toml`;
  - the `.pyi` stubs are generated at build time by `hatch-reflex-pyi` and are
    no longer committed;
  - pre-commit runs ruff, pyright and file checks; new `AGENTS.md`.
- Python 3.14 is supported and tested.
- CI runs pre-commit (with pyright) instead of bare ruff, and the release
  workflow checks that the built version matches the tag and that the wheel
  ships the stub.

### Fixed

- Type checkers no longer require every field of `Step`, `TourOptions`,
  `Locale`, `TourStyles`, `FloatingOptions` and `SpotlightPadding`: all fields
  default to `None`, so `TourOptions(z_index=1000)` type-checks. Serialization
  is unchanged.
- `steps` is typed as a sequence of `Step` objects or dicts, so passing
  `[rjr.Step(...)]` or a `list[dict]` State var no longer shows a type error.
- `options`, `locale`, `styles` and `floating_options` accept their typed
  objects (`TourOptions`, `Locale`, `TourStyles`, `FloatingOptions`) in the
  stubs, matching the documented usage.

## [0.2.0] - 2026-10-25

### Changed

- Requires **Reflex 0.10.0** or newer (was 0.9.11).
- Requires **Python 3.11** or newer; Python 3.10 is no longer supported, in
  line with Reflex 0.10.
- Build backend requires `setuptools>=78.1.1`.
- CI and release workflows use Node 24 (`.nvmrc`), and every JavaScript action
  is forced onto the Node 24 runtime.
- The release workflow only publishes tags that point to a commit on `main`.
- `reflex component build` no longer exists in Reflex 0.10: build with
  `uv build` and regenerate the `.pyi` stubs with
  `python -m reflex_base.utils.pyi_generator` (see the README).
- Regenerated `joyride.pyi`, so the `tooltip` docstring matches the source.

### Unchanged

- The Python API (`joyride`, props, actions, events and constants) and the
  bundled react-joyride 3.2.0 are the same as in 0.1.0.

## [0.1.0] - 2026-09-17

### Added

- First release: Reflex wrapper for react-joyride 3.2.0 with typed props,
  controlled and uncontrolled modes, Python actions, per-event triggers,
  custom tooltip and beacon components, and a four page demo app.

[0.3.0]: https://github.com/ecrespo/reflex-react-joyride/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/ecrespo/reflex-react-joyride/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/ecrespo/reflex-react-joyride/releases/tag/v0.1.0
