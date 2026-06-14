"""TDD tests for the pie/donut family wrappers."""

import reflex as rx

_CATEGORY_SAMPLE = [{"name": "AAPL", "value": 30}]

_PIE_FUNCS = [
    "pie_chart",
    "pie_chart_stocks",
    "pie_chart_labels",
    "donut_chart",
    "donut_chart_center_text",
    "donut_chart_half",
    "donut_chart_fillable_half",
    "donut_chart_fillable",
]


def _default_data(comp: rx.Component):
    return comp.data._var_value if hasattr(comp.data, "_var_value") else None


def test_all_pie_funcs_exported():
    import reflex_rosencharts as rxc

    for fn in _PIE_FUNCS:
        assert hasattr(rxc, fn), f"{fn} must be re-exported from the package root"


def test_pie_chart_builds_and_default():
    import reflex_rosencharts as rxc

    comp = rxc.pie_chart(data=_CATEGORY_SAMPLE)
    assert isinstance(comp, rx.Component)
    assert len(_default_data(rxc.pie_chart())) > 0


def test_pie_chart_stocks_builds_and_default():
    import reflex_rosencharts as rxc

    comp = rxc.pie_chart_stocks(
        data=[
            {
                "name": "Apple",
                "value": 731,
                "logo": "x.svg",
                "color": "text-pink-400",
            }
        ]
    )
    assert isinstance(comp, rx.Component)
    assert len(_default_data(rxc.pie_chart_stocks())) > 0


def test_pie_chart_labels_builds_and_default():
    import reflex_rosencharts as rxc

    comp = rxc.pie_chart_labels(
        data=[
            {
                "name": "Technology",
                "value": 731,
                "colorFrom": "text-pink-400",
                "colorTo": "text-pink-400",
            }
        ]
    )
    assert isinstance(comp, rx.Component)
    assert len(_default_data(rxc.pie_chart_labels())) > 0


def test_donut_chart_builds_and_default():
    import reflex_rosencharts as rxc

    comp = rxc.donut_chart(data=_CATEGORY_SAMPLE)
    assert isinstance(comp, rx.Component)
    assert len(_default_data(rxc.donut_chart())) > 0


def test_donut_chart_center_text_builds_and_default():
    import reflex_rosencharts as rxc

    comp = rxc.donut_chart_center_text(data=_CATEGORY_SAMPLE, center_text="200")
    assert isinstance(comp, rx.Component)
    assert len(_default_data(rxc.donut_chart_center_text())) > 0


def test_donut_chart_half_builds_and_default():
    import reflex_rosencharts as rxc

    comp = rxc.donut_chart_half(data=_CATEGORY_SAMPLE)
    assert isinstance(comp, rx.Component)
    assert len(_default_data(rxc.donut_chart_half())) > 0


def test_donut_chart_fillable_half_builds_and_default():
    import reflex_rosencharts as rxc

    comp = rxc.donut_chart_fillable_half(value=42)
    assert isinstance(comp, rx.Component)
    # default value prop must be present and > 0
    val = comp.value._var_value if hasattr(comp.value, "_var_value") else None
    default_comp = rxc.donut_chart_fillable_half()
    dval = (
        default_comp.value._var_value
        if hasattr(default_comp.value, "_var_value")
        else None
    )
    assert dval is not None and dval > 0


def test_donut_chart_fillable_builds_and_default():
    import reflex_rosencharts as rxc

    comp = rxc.donut_chart_fillable(value=42)
    assert isinstance(comp, rx.Component)
    default_comp = rxc.donut_chart_fillable()
    dval = (
        default_comp.value._var_value
        if hasattr(default_comp.value, "_var_value")
        else None
    )
    assert dval is not None and dval > 0
