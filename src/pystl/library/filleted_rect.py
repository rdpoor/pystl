"""Filleted rectangle parts."""

from dataclasses import dataclass

from solid2 import circle, polygon
from solid2.core.object_base import OpenSCADObject

from pystl.py_stl_geometry import PyStlGeometry
from pystl.py_stl_part import PyStlPart


def filleted_rect(
    width: float,
    height: float,
    radius: float,
    fn: int = 64,
) -> OpenSCADObject:
    """A 2D rectangle with filleted corners, centered at the origin.

    Args:
        width: Width of the rectangle.
        height: Height of the rectangle.
        radius: Radius of the four corner fillets.
        fn: Fragment count for fillet circles.

    Returns:
        A 2D OpenSCAD object.
    """
    w2 = width / 2.0
    h2 = height / 2.0
    r = radius
    fillet = circle(r, _fn=fn)
    south_west = fillet.translate([-w2 + r, -h2 + r, 0])
    south_east = fillet.translate([w2 - r, -h2 + r, 0])
    north_east = fillet.translate([w2 - r, h2 - r, 0])
    north_west = fillet.translate([-w2 + r, h2 - r, 0])
    body = polygon(
        [
            [-w2 + r, -h2],
            [w2 - r, -h2],
            [w2, -h2 + r],
            [w2, h2 - r],
            [w2 - r, h2],
            [-w2 + r, h2],
            [-w2, h2 - r],
            [-w2, -h2 + r],
            [-w2 + r, -h2],
        ]
    )
    return body + south_west + south_east + north_east + north_west


@dataclass
class FilletedRect(PyStlPart):
    """A 3D rectangle with filleted corners, extruded to a given depth.

    Attributes:
        width: Width of the rectangle.
        height: Height of the rectangle.
        radius: Radius of the four corner fillets.
        depth: Extrusion depth along the z-axis.
        fn: Fragment count for fillet circles.
    """

    width: float = 40.0
    height: float = 30.0
    radius: float = 5.0
    depth: float = 1.0
    fn: int = 64

    def build(self) -> PyStlGeometry:
        """Build the 3D filleted rectangle.

        Returns:
            Geometry representing the extruded filleted rectangle.
        """
        return PyStlGeometry(
            positive=filleted_rect(self.width, self.height, self.radius, self.fn),
            negative=None,
        ).linear_extrude(self.depth)


@dataclass
class FilletedFrame(PyStlPart):
    """A 3D frame: an outer filleted rect with an inner one subtracted, extruded.

    The inner dimensions are derived from the outer dimensions and
    ``frame_thickness``. At least one of ``inner_radius`` or
    ``outer_radius`` must be provided; the other is derived using
    ``outer_radius = inner_radius + frame_thickness / 2``.

    Attributes:
        outer_width: Width of the outer rectangle.
        outer_height: Height of the outer rectangle.
        frame_thickness: Uniform wall thickness (outer minus inner, per side).
        depth: Extrusion depth along the z-axis.
        outer_radius: Fillet radius of the outer rectangle.
        inner_radius: Fillet radius of the inner cutout rectangle.
        fn: Fragment count for fillet circles.
    """

    outer_width: float = 40.0
    outer_height: float = 30.0
    frame_thickness: float = 5.0
    depth: float = 1.0
    outer_radius: float | None = None
    inner_radius: float | None = None
    fn: int = 64

    def __post_init__(self) -> None:
        """Derive the missing radius, or raise if both are absent."""
        if self.outer_radius is None and self.inner_radius is None:
            raise ValueError(
                "at least one of outer_radius or inner_radius must be specified"
            )
        if self.outer_radius is None:
            self.outer_radius = self.inner_radius + self.frame_thickness
        if self.inner_radius is None:
            self.inner_radius = self.outer_radius - self.frame_thickness

    def build(self) -> PyStlGeometry:
        """Build the 3D filleted frame.

        Returns:
            Geometry representing the extruded filleted frame.
        """
        inner_width = self.outer_width - self.frame_thickness * 2
        inner_height = self.outer_height - self.frame_thickness * 2
        outer = filleted_rect(
            self.outer_width, self.outer_height, self.outer_radius, self.fn
        )
        cutout = filleted_rect(
            inner_width, inner_height, self.inner_radius, self.fn
        )
        return PyStlGeometry(
            positive=outer.linear_extrude(self.depth),
            negative=cutout.linear_extrude(self.depth + self.CUT_CLEARANCE),
        )
