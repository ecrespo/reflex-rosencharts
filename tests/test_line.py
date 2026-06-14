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


# --- line_chart_curved -------------------------------------------------------


def test_line_chart_curved_is_exported():
    import reflex_rosencharts as rxc

    assert hasattr(rxc, "line_chart_curved")


def test_line_chart_curved_builds_component():
    import reflex_rosencharts as rxc

    comp = rxc.line_chart_curved(data=[{"date": "2023-05-01", "value": 6}])
    assert isinstance(comp, rx.Component)


def test_line_chart_curved_has_default_data():
    import reflex_rosencharts as rxc

    comp = rxc.line_chart_curved()
    default = comp.data._var_value if hasattr(comp.data, "_var_value") else None
    assert default is not None
    assert len(default) > 0


# --- line_chart_multiple -----------------------------------------------------


def test_line_chart_multiple_is_exported():
    import reflex_rosencharts as rxc

    assert hasattr(rxc, "line_chart_multiple")


def test_line_chart_multiple_builds_component():
    import reflex_rosencharts as rxc

    comp = rxc.line_chart_multiple(
        data=[{"date": "2023-05-01", "value": 6}],
        data2=[{"date": "2023-05-01", "value": 3}],
    )
    assert isinstance(comp, rx.Component)


def test_line_chart_multiple_has_default_data():
    import reflex_rosencharts as rxc

    comp = rxc.line_chart_multiple()
    default = comp.data._var_value if hasattr(comp.data, "_var_value") else None
    assert default is not None
    assert len(default) > 0


# --- line_chart_labels_curved ------------------------------------------------


def test_line_chart_labels_curved_is_exported():
    import reflex_rosencharts as rxc

    assert hasattr(rxc, "line_chart_labels_curved")


def test_line_chart_labels_curved_builds_component():
    import reflex_rosencharts as rxc

    comp = rxc.line_chart_labels_curved(data=[{"date": "2023-05-01", "value": 6}])
    assert isinstance(comp, rx.Component)


def test_line_chart_labels_curved_has_default_data():
    import reflex_rosencharts as rxc

    comp = rxc.line_chart_labels_curved()
    default = comp.data._var_value if hasattr(comp.data, "_var_value") else None
    assert default is not None
    assert len(default) > 0


# --- line_chart_stocks_curved ------------------------------------------------


def test_line_chart_stocks_curved_is_exported():
    import reflex_rosencharts as rxc

    assert hasattr(rxc, "line_chart_stocks_curved")


def test_line_chart_stocks_curved_builds_component():
    import reflex_rosencharts as rxc

    comp = rxc.line_chart_stocks_curved(data=[{"date": "2023-05-01", "value": 6}])
    assert isinstance(comp, rx.Component)


def test_line_chart_stocks_curved_has_default_data():
    import reflex_rosencharts as rxc

    comp = rxc.line_chart_stocks_curved()
    default = comp.data._var_value if hasattr(comp.data, "_var_value") else None
    assert default is not None
    assert len(default) > 0


# --- line_chart_step ---------------------------------------------------------


def test_line_chart_step_is_exported():
    import reflex_rosencharts as rxc

    assert hasattr(rxc, "line_chart_step")


def test_line_chart_step_builds_component():
    import reflex_rosencharts as rxc

    comp = rxc.line_chart_step(data=[{"date": "2023-05-01", "value": 6}])
    assert isinstance(comp, rx.Component)


def test_line_chart_step_has_default_data():
    import reflex_rosencharts as rxc

    comp = rxc.line_chart_step()
    default = comp.data._var_value if hasattr(comp.data, "_var_value") else None
    assert default is not None
    assert len(default) > 0


# --- line_chart_pulse --------------------------------------------------------


def test_line_chart_pulse_is_exported():
    import reflex_rosencharts as rxc

    assert hasattr(rxc, "line_chart_pulse")


def test_line_chart_pulse_builds_component():
    import reflex_rosencharts as rxc

    comp = rxc.line_chart_pulse(data=[{"date": "2023-05-01", "value": 6}])
    assert isinstance(comp, rx.Component)


def test_line_chart_pulse_has_default_data():
    import reflex_rosencharts as rxc

    comp = rxc.line_chart_pulse()
    default = comp.data._var_value if hasattr(comp.data, "_var_value") else None
    assert default is not None
    assert len(default) > 0


# --- line_chart_full ---------------------------------------------------------


def test_line_chart_full_is_exported():
    import reflex_rosencharts as rxc

    assert hasattr(rxc, "line_chart_full")


def test_line_chart_full_builds_component():
    import reflex_rosencharts as rxc

    comp = rxc.line_chart_full(data=[{"date": "2023-05-01", "value": 6}])
    assert isinstance(comp, rx.Component)


def test_line_chart_full_has_default_data():
    import reflex_rosencharts as rxc

    comp = rxc.line_chart_full()
    default = comp.data._var_value if hasattr(comp.data, "_var_value") else None
    assert default is not None
    assert len(default) > 0
