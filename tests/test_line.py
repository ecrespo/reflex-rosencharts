"""TDD tests for the line family wrappers."""

import reflex as rx


def test_line_chart_is_exported():
    import reflex_rosencharts as rxc

    assert hasattr(rxc, "line_chart"), "line_chart must be re-exported from the package root"


def test_line_chart_builds_component():
    import reflex_rosencharts as rxc

    comp = rxc.line_chart(data=[{"date": "2023-05-01", "value": 6}])
    assert isinstance(comp, rx.Component)


def test_line_chart_has_default_data_matching_example():
    import reflex_rosencharts as rxc

    comp = rxc.line_chart()  # no args → reproduces the original example
    # The default data var must be present and non-empty (10 points in the original).
    default = comp.data._var_value if hasattr(comp.data, "_var_value") else None
    assert default is not None
    assert len(default) == 10
