"""TDD tests for the area family wrappers."""

import reflex as rx

_SAMPLE = [{"date": "2023-05-01", "value": 6}]

_CHARTS = [
    "area_chart",
    "area_chart_full",
    "area_chart_gradient",
    "area_chart_semi_filled",
]


def test_area_charts_exported():
    import reflex_rosencharts as rxc

    for name in _CHARTS:
        assert hasattr(rxc, name), f"{name} must be re-exported from the package root"


def test_area_charts_build_component():
    import reflex_rosencharts as rxc

    for name in _CHARTS:
        fn = getattr(rxc, name)
        comp = fn(data=_SAMPLE)
        assert isinstance(comp, rx.Component), f"{name}(data=...) must build a Component"


def test_area_charts_have_default_data():
    import reflex_rosencharts as rxc

    for name in _CHARTS:
        fn = getattr(rxc, name)
        comp = fn()  # no args → reproduces the original example
        default = comp.data._var_value if hasattr(comp.data, "_var_value") else None
        assert default is not None, f"{name}() must expose default data var"
        assert len(default) > 0, f"{name}() default data must be non-empty"
