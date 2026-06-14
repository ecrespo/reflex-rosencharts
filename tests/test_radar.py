"""TDD tests for the radar family wrappers."""

import reflex as rx

_SAMPLE = [{"topic": "Tech", "value": 330}]


def _default_data(comp: rx.Component):
    return comp.data._var_value if hasattr(comp.data, "_var_value") else None


# --- radar_chart ---------------------------------------------------------


def test_radar_chart_is_exported():
    import reflex_rosencharts as rxc

    assert hasattr(rxc, "radar_chart"), "radar_chart must be re-exported from the package root"


def test_radar_chart_builds_component():
    import reflex_rosencharts as rxc

    comp = rxc.radar_chart(data=_SAMPLE)
    assert isinstance(comp, rx.Component)


def test_radar_chart_has_default_data():
    import reflex_rosencharts as rxc

    comp = rxc.radar_chart()  # no args → reproduces the original example
    default = _default_data(comp)
    assert default is not None
    assert len(default) == 5


# --- radar_chart_rounded -------------------------------------------------


def test_radar_chart_rounded_is_exported():
    import reflex_rosencharts as rxc

    assert hasattr(rxc, "radar_chart_rounded")


def test_radar_chart_rounded_builds_component():
    import reflex_rosencharts as rxc

    comp = rxc.radar_chart_rounded(data=_SAMPLE)
    assert isinstance(comp, rx.Component)


def test_radar_chart_rounded_has_default_data():
    import reflex_rosencharts as rxc

    comp = rxc.radar_chart_rounded()
    default = _default_data(comp)
    assert default is not None
    assert len(default) == 5
