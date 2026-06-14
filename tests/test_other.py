"""TDD tests for the other family wrappers (bubble_chart, funnel_chart)."""

import reflex as rx


# --- bubble_chart -----------------------------------------------------------


def test_bubble_chart_is_exported():
    import reflex_rosencharts as rxc

    assert hasattr(rxc, "bubble_chart"), "bubble_chart must be re-exported from the package root"


def test_bubble_chart_builds_component():
    import reflex_rosencharts as rxc

    comp = rxc.bubble_chart(data=[{"name": "MacOS", "sector": "Tech", "value": 4812}])
    assert isinstance(comp, rx.Component)


def test_bubble_chart_has_non_empty_default_data():
    import reflex_rosencharts as rxc

    comp = rxc.bubble_chart()  # no args → reproduces the original example
    default = comp.data._var_value if hasattr(comp.data, "_var_value") else None
    assert default is not None
    assert len(default) > 0


# --- funnel_chart -----------------------------------------------------------


def test_funnel_chart_is_exported():
    import reflex_rosencharts as rxc

    assert hasattr(rxc, "funnel_chart"), "funnel_chart must be re-exported from the package root"


def test_funnel_chart_builds_component():
    import reflex_rosencharts as rxc

    comp = rxc.funnel_chart(data=[{"name": "Gross Revenue", "value": 47.1}])
    assert isinstance(comp, rx.Component)


def test_funnel_chart_has_non_empty_default_data():
    import reflex_rosencharts as rxc

    comp = rxc.funnel_chart()  # no args → reproduces the original example
    default = comp.data._var_value if hasattr(comp.data, "_var_value") else None
    assert default is not None
    assert len(default) > 0
