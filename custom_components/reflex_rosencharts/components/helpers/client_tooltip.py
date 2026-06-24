"""Registers the shared ``ClientTooltip.tsx`` helper as a frontend asset.

The chart TSX files import the tooltip via the absolute ``$/public/...`` alias
that Reflex generates (see ``CLIENT_TOOLTIP_IMPORT``) rather than a relative
path, because each chart TSX is symlinked into its own module-named directory
under ``assets/external/`` and a relative ``../helpers`` path would not resolve.

Importing this module (done from every chart wrapper) is what triggers the
symlink, so the helper is present in the compiled frontend.
"""

import reflex as rx

# Symlinked to assets/external/reflex_rosencharts/components/helpers/client_tooltip/ClientTooltip.tsx
_path = rx.asset("./ClientTooltip.tsx", shared=True)

# Build-time module reference used inside the chart .tsx import statements.
CLIENT_TOOLTIP_IMPORT = f"$/public{_path}"
