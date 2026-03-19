"""Geometry utilities for pystl models."""

from solid2 import cube
from solid2.core.object_base import OpenSCADObject

# Half-space cutter extent in mm — large enough to cover any printable part.
_HALF_SPACE: float = 1000.0


def split_at_y(obj: OpenSCADObject) -> tuple[OpenSCADObject, OpenSCADObject]:
    """Split an OpenSCADObject into two halves along the Y=0 plane.

    Args:
        obj: The model to split.

    Returns:
        A tuple ``(negative, positive)`` where:
        - ``negative`` contains all geometry with y < 0
        - ``positive`` contains all geometry with y >= 0
    """
    s = _HALF_SPACE
    positive_half = cube([2 * s, s, 2 * s]).translate([-s, 0, -s])
    negative_half = cube([2 * s, s, 2 * s]).translate([-s, -s, -s])
    return obj * negative_half, obj * positive_half
