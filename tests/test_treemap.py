"""TDD tests for the treemap family wrappers."""

import reflex as rx

_SAMPLE = [{"topic": "Tech", "subtopics": [{"Windows": 100, "MacOS": 120}]}]
_SAMPLE_IMAGES = [
    {
        "topic": "Tech",
        "subtopics": [{"name": "Apple", "value": 100, "logo": "https://example.com/a.svg"}],
    }
]


def _default(comp):
    return comp.data._var_value if hasattr(comp.data, "_var_value") else None


# --- treemap_chart -----------------------------------------------------------
def test_treemap_chart_is_exported():
    import reflex_rosencharts as rxc

    assert hasattr(rxc, "treemap_chart")


def test_treemap_chart_builds_component():
    import reflex_rosencharts as rxc

    comp = rxc.treemap_chart(data=_SAMPLE)
    assert isinstance(comp, rx.Component)


def test_treemap_chart_has_default_data():
    import reflex_rosencharts as rxc

    comp = rxc.treemap_chart()
    default = _default(comp)
    assert default is not None
    assert len(default) > 0


# --- treemap_chart_images ----------------------------------------------------
def test_treemap_chart_images_is_exported():
    import reflex_rosencharts as rxc

    assert hasattr(rxc, "treemap_chart_images")


def test_treemap_chart_images_builds_component():
    import reflex_rosencharts as rxc

    comp = rxc.treemap_chart_images(data=_SAMPLE_IMAGES)
    assert isinstance(comp, rx.Component)


def test_treemap_chart_images_has_default_data():
    import reflex_rosencharts as rxc

    comp = rxc.treemap_chart_images()
    default = _default(comp)
    assert default is not None
    assert len(default) > 0


# --- treemap_chart_gradient --------------------------------------------------
def test_treemap_chart_gradient_is_exported():
    import reflex_rosencharts as rxc

    assert hasattr(rxc, "treemap_chart_gradient")


def test_treemap_chart_gradient_builds_component():
    import reflex_rosencharts as rxc

    comp = rxc.treemap_chart_gradient(data=_SAMPLE)
    assert isinstance(comp, rx.Component)


def test_treemap_chart_gradient_has_default_data():
    import reflex_rosencharts as rxc

    comp = rxc.treemap_chart_gradient()
    default = _default(comp)
    assert default is not None
    assert len(default) > 0
