"""Smoke tests for the public API: every exported chart builds and renders."""

import re
import tomllib
from pathlib import Path

import pytest
import reflex as rx

import reflex_rosencharts as rxc

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "custom_components" / "reflex_rosencharts"

# Public factory functions (snake_case); the component classes are exported too.
CHARTS = sorted(
    name for name in rxc.__all__ if name.islower() and name != "rosen_chart"
)

AXIS_CHARTS = [
    "scatter_chart",
    "scatter_chart_interactive",
    "scatter_chart_multiclass",
    "scatter_chart_stocks",
]
MARGIN_CHARTS = [
    *AXIS_CHARTS,
    "line_chart",
    "line_chart_curved",
    "line_chart_multiple",
    "line_chart_pulse",
    "line_chart_step",
    "line_chart_stocks_curved",
]


def test_exports_all_43_charts():
    assert len(CHARTS) == 43


def test_version_matches_pyproject():
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text())
    assert rxc.__version__ == pyproject["project"]["version"]


@pytest.mark.parametrize("name", CHARTS)
def test_chart_builds_with_defaults(name):
    component = getattr(rxc, name)()
    assert isinstance(component, rx.Component)
    assert component.tag
    rendered = component.render()
    assert rendered["name"]


@pytest.mark.parametrize("name", CHARTS)
def test_chart_library_points_to_existing_tsx(name):
    component = getattr(rxc, name)()
    library = component.library
    assert library.startswith("$/public/external/reflex_rosencharts/components/")
    assert library.endswith(".tsx")
    # "$/public/external/.../components/<family>/<module>/<File>.tsx"
    parts = library.split("/components/")[1].split("/")
    source = PACKAGE / "components" / parts[0] / parts[-1]
    assert source.is_file(), source


@pytest.mark.parametrize("name", MARGIN_CHARTS)
def test_margin_left_prop_is_camel_cased(name):
    props = str(getattr(rxc, name)(margin_left="46px").render()["props"])
    assert "marginLeft" in props


X_TICK_CHARTS = [
    "area_chart",
    "line_chart",
    "line_chart_curved",
    "line_chart_labels_curved",
    "line_chart_multiple",
    "line_chart_pulse",
    "line_chart_step",
    "line_chart_stocks_curved",
]


@pytest.mark.parametrize("name", X_TICK_CHARTS)
def test_x_ticks_prop_is_camel_cased(name):
    props = str(getattr(rxc, name)(x_ticks="regular").render()["props"])
    assert "xTicks" in props


@pytest.mark.parametrize("name", X_TICK_CHARTS)
def test_x_ticks_tsx_uses_shared_label_helper(name):
    library = getattr(rxc, name)().library
    parts = library.split("/components/")[1].split("/")
    source = (PACKAGE / "components" / parts[0] / parts[-1]).read_text()
    assert "xAxisLabels(" in source
    assert "isMax" not in source


@pytest.mark.parametrize("name", AXIS_CHARTS)
def test_scale_props_are_camel_cased(name):
    props = str(getattr(rxc, name)(x_scale="log", y_scale="symlog").render()["props"])
    assert "xScale" in props
    assert "yScale" in props


def test_tsx_imports_do_not_use_relative_helper_paths():
    # Chart TSX files are symlinked into per-module directories, so a relative
    # "../helpers" import would not resolve in the compiled frontend.
    offenders = [
        str(path.relative_to(ROOT))
        for path in PACKAGE.rglob("*.tsx")
        if re.search(r"from\s+['\"]\.\.?/", path.read_text())
    ]
    assert offenders == []
