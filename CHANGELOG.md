# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses
[Semantic Versioning](https://semver.org/).

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

[0.2.0]: https://github.com/ecrespo/reflex-react-joyride/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/ecrespo/reflex-react-joyride/releases/tag/v0.1.0
