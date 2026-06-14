"""Smoke tests: the package and its public API are importable."""


def test_package_imports():
    import reflex_rosencharts as rxc

    assert hasattr(rxc, "__version__")
