"""Inset sub-parts (recessed features) for pystl models."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Optional

import numpy as np
from solid2 import circle, cylinder, linear_extrude, polygon
from solid2.core.object_base import OpenSCADObject

from pystl.library import hex_nuts
from pystl.py_stl_geometry import PyStlGeometry
from pystl.py_stl_part import PyStlPart


@dataclass
class PyStlInset(PyStlPart):
    """Base class for inset features embedded into a part face.

    By convention, the inset is centered at x=0, y=0 and extends
    ``depth`` units into the -z plane.
    """

    depth: float = 1

    def build(self) -> PyStlGeometry:
        """Return ``(part, hole)`` geometry for this inset.

        Raises:
            NotImplementedError: Subclasses must implement this method.
        """
        raise NotImplementedError


@dataclass
class HexNutInset(PyStlInset):
    """Recessed hex-nut trap, centered at the origin."""

    nut: Optional[hex_nuts.HexNut] = None

    def build(self) -> PyStlGeometry:
        inset = cylinder(
            h=self.depth + self.CUT_CLEARANCE, d=self.nut.inset_diameter, _fn=6
        ).translate([0, 0, -self.depth])
        return PyStlGeometry(positive=None, negative=inset)

# Usage
# from pystl.library import hex_nuts
# m12 = hex_nuts.get('M12')
# inset = HexNutInset(nut=m12, depth=m12.thickness_nom)

@dataclass
class CircularInset(PyStlInset):
    """Recessed circle, centered at the origin."""

    diameter: float = 6.0
    fn: int = 64

    def build(self) -> PyStlGeometry:
        inset = cylinder(
            h=self.depth + self.CUT_CLEARANCE, d=self.diameter, _fn=self.fn
        ).translate([0, 0, -self.depth])
        return PyStlGeometry(positive=None, negative=inset)

@dataclass
class CountersinkInset(PyStlInset):
    """90 degree countersink inset for flat head bolts"""
    diameter: float = 6.0
    fn: int = 64

    def build(self) -> PyStlGeometry:
        d2 = self.diameter
        # 45° half-angle -> radius decreases 1:1 with depth
        d1 = max(0.0, d2 - 2.0 * self.depth)
        # Extend cone by CUT_CLEARANCE above z=0; d2 remains the diameter
        # at z=0, so the top diameter grows by 2*CUT_CLEARANCE.
        d_top = d2 + 2.0 * self.CUT_CLEARANCE
        h = self.depth + self.CUT_CLEARANCE
        inset = cylinder(h=h, d1=d1, d2=d_top, _fn=self.fn).translate(
            [0, 0, -self.depth]
        )
        return PyStlGeometry(positive=None, negative=inset)


def slotted_arc(
    start_deg: float,
    end_deg: float,
    radius: float,
    slot_width: float,
    fn: int = 128,
) -> OpenSCADObject:
    """Create a 2D slotted arc centered at the origin.

    Args:
        start_deg: Starting angle of arc (degrees, 0–360).
        end_deg: Ending angle of arc (degrees, 0–360).
        radius: Distance from origin to center of the arc's slot.
        slot_width: Width of the slot.
        fn: Number of polygon steps to create the arc.

    Returns:
        A 2D OpenSCAD object representing the slotted arc.
    """
    def _dtor(degree: float) -> float:
        return degree * math.pi / 180.0

    k = max(3, fn)
    thetas = [_dtor(d) for d in np.linspace(start_deg, end_deg, k)]

    r0 = radius - slot_width / 2.0
    r1 = radius + slot_width / 2.0

    inner = [
        [r0 * math.cos(t), r0 * math.sin(t)]
        for t in thetas
    ]
    outer = [
        [r1 * math.cos(t), r1 * math.sin(t)]
        for t in reversed(thetas)
    ]

    end_cap = circle(r=slot_width / 2, _fn=fn)
    e0 = end_cap.translate(
        [radius * math.cos(thetas[0]), radius * math.sin(thetas[0]), 0]
    )
    e1 = end_cap.translate(
        [radius * math.cos(thetas[-1]), radius * math.sin(thetas[-1]), 0]
    )
    return polygon(inner + outer) + e0 + e1


@dataclass
class SlottedArcInset(PyStlInset):
    """Recessed slotted-arc channel, extruded to ``depth``.

    The arc is defined in the XY plane and extruded along -Z. All
    positional arguments are relative to the inset origin.

    Attributes:
        start_deg: Starting angle of the arc (degrees, 0–360).
        end_deg: Ending angle of the arc (degrees, 0–360).
        radius: Distance from origin to the center-line of the slot.
        slot_width: Width of the slot.
        fn: Fragment count for arc and end-cap circles.
    """

    start_deg: float = 0.0
    end_deg: float = 90.0
    radius: float = 10.0
    slot_width: float = 2.0
    fn: int = 128

    def build(self) -> PyStlGeometry:
        arc_2d = slotted_arc(
            start_deg=self.start_deg,
            end_deg=self.end_deg,
            radius=self.radius,
            slot_width=self.slot_width,
            fn=self.fn,
        )
        inset = (
            linear_extrude(self.depth + self.CUT_CLEARANCE)(arc_2d)
            .translate([0, 0, -self.depth])
        )
        return PyStlGeometry(positive=None, negative=inset)
