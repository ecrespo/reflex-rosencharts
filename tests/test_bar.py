"""TDD tests for the bar chart family.

For every ported chart: the function is exported from ``reflex_rosencharts``,
``fn(data=[...one sample row...])`` builds an ``rx.Component``, and ``fn()`` with no
args has non-empty default data.
"""

import reflex as rx

import reflex_rosencharts as rxc


def _assert_chart(fn, sample_row: dict) -> None:
    """A chart function builds a component from data and ships non-empty defaults."""
    comp = fn(data=[sample_row])
    assert isinstance(comp, rx.Component)

    default = fn()
    assert isinstance(default, rx.Component)
    # Non-empty default data (the original rosencharts example).
    assert default.data._var_value  # type: ignore[attr-defined]


def test_bar_chart_horizontal():
    _assert_chart(rxc.bar_chart_horizontal, {"key": "Tech", "value": 38.1})


def test_bar_chart_horizontal_logo():
    _assert_chart(
        rxc.bar_chart_horizontal_logo,
        {"key": "Company A", "value": 55.8, "color": "bg-pink-300"},
    )


def test_bar_chart_gradient():
    _assert_chart(
        rxc.bar_chart_gradient,
        {"key": "Tech", "value": 38.1, "color": "from-pink-300 to-pink-400"},
    )


def test_bar_chart_breakdown():
    _assert_chart(
        rxc.bar_chart_breakdown,
        {"key": "Tech", "value": 17.1, "color": "from-violet-300 to-violet-400"},
    )


def test_bar_chart_thin_breakdown():
    _assert_chart(
        rxc.bar_chart_thin_breakdown,
        {"key": "Tech", "value": 17.1, "color": "from-violet-300 to-violet-400"},
    )


def test_bar_chart_thin_horizontal():
    _assert_chart(rxc.bar_chart_thin_horizontal, {"key": "France", "value": 38.1})


def test_bar_chart_flags_horizontal():
    _assert_chart(
        rxc.bar_chart_flags_horizontal,
        {"key": "Portugal", "value": 55.8, "flag": "pt"},
    )


def test_bar_chart_vertical():
    _assert_chart(rxc.bar_chart_vertical, {"key": "Tech", "value": 18.1})


def test_bar_chart_multi_vertical():
    _assert_chart(
        rxc.bar_chart_multi_vertical,
        {"key": "Jan 2020", "values": [11.1, 9.5]},
    )


def test_bar_chart_triple_flags_horizontal():
    _assert_chart(
        rxc.bar_chart_triple_flags_horizontal,
        {"key": "European Union", "values": [15, 25, 33], "flag": "eu"},
    )


def test_bar_chart_line():
    _assert_chart(
        rxc.bar_chart_line,
        {"key": "Jan", "metric1": 18.1, "metric2": 700},
    )


def test_bar_chart_benchmark():
    _assert_chart(rxc.bar_chart_benchmark, {"key": "Model 0", "value": 85.8})
