"""Shared ClientTooltip helper (ported from rosencharts helpers/ClientTooltip.tsx).

The TSX exports ``ClientTooltip``, ``TooltipTrigger`` and ``TooltipContent`` and is
imported *inside* each chart TSX (not composed from Python). Its only job on the
Python side is to make sure the ``.tsx`` file ships into the generated frontend so
that a chart's ``../helpers/ClientTooltip`` relative import resolves.

``rx.asset`` resolves the path relative to the file that calls it, which is why this
module lives next to ``ClientTooltip.tsx``.
"""

import reflex as rx


def client_tooltip_asset() -> str:
    """Register the ClientTooltip TSX as a shared asset and return its public path."""
    return rx.asset("ClientTooltip.tsx", shared=True)
