"""TDD tests for the scatter family wrappers."""

import reflex as rx

_SAMPLE = [{"revenue": 10, "value": 102.8, "company": "Company A"}]


def _default(comp):
    return comp.data._var_value if hasattr(comp.data, "_var_value") else None


# scatter_chart ---------------------------------------------------------------
def test_scatter_chart_is_exported():
    import reflex_rosencharts as rxc

    assert hasattr(rxc, "scatter_chart")


def test_scatter_chart_builds_component():
    import reflex_rosencharts as rxc

    comp = rxc.scatter_chart(data=_SAMPLE)
    assert isinstance(comp, rx.Component)


def test_scatter_chart_has_default_data():
    import reflex_rosencharts as rxc

    comp = rxc.scatter_chart()
    default = _default(comp)
    assert default is not None and len(default) > 0


# scatter_chart_interactive ---------------------------------------------------
def test_scatter_chart_interactive_is_exported():
    import reflex_rosencharts as rxc

    assert hasattr(rxc, "scatter_chart_interactive")


def test_scatter_chart_interactive_builds_component():
    import reflex_rosencharts as rxc

    comp = rxc.scatter_chart_interactive(data=_SAMPLE)
    assert isinstance(comp, rx.Component)


def test_scatter_chart_interactive_has_default_data():
    import reflex_rosencharts as rxc

    comp = rxc.scatter_chart_interactive()
    default = _default(comp)
    assert default is not None and len(default) > 0


def test_scatter_chart_interactive_has_click_handler():
    import reflex_rosencharts as rxc

    comp = rxc.scatter_chart_interactive(data=_SAMPLE)
    assert "on_point_click" in comp.get_event_triggers()


# scatter_chart_multiclass ----------------------------------------------------
def test_scatter_chart_multiclass_is_exported():
    import reflex_rosencharts as rxc

    assert hasattr(rxc, "scatter_chart_multiclass")


def test_scatter_chart_multiclass_builds_component():
    import reflex_rosencharts as rxc

    comp = rxc.scatter_chart_multiclass(
        data=[{"revenue": 10, "value": 102.8, "company": "Green A", "class": "green"}]
    )
    assert isinstance(comp, rx.Component)


def test_scatter_chart_multiclass_has_default_data():
    import reflex_rosencharts as rxc

    comp = rxc.scatter_chart_multiclass()
    default = _default(comp)
    assert default is not None and len(default) > 0


# scatter_chart_stocks --------------------------------------------------------
def test_scatter_chart_stocks_is_exported():
    import reflex_rosencharts as rxc

    assert hasattr(rxc, "scatter_chart_stocks")


def test_scatter_chart_stocks_builds_component():
    import reflex_rosencharts as rxc

    comp = rxc.scatter_chart_stocks(data=[{"revenue": 10, "value": 500, "company": "Company A"}])
    assert isinstance(comp, rx.Component)


def test_scatter_chart_stocks_has_default_data():
    import reflex_rosencharts as rxc

    comp = rxc.scatter_chart_stocks()
    default = _default(comp)
    assert default is not None and len(default) > 0
