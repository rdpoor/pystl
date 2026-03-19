"""General pipe clamp v1.0"""

import logging
import math
from dataclasses import dataclass

from solid2 import cube, cylinder
from solid2.core.object_base import OpenSCADObject

from pystl.py_stl_base import PyStlPart

log = logging.getLogger(__name__)


@dataclass
class GeneralPipeClamp(PyStlPart):
    """A general purpose pipe clamp with two mouting tabs.

    Attributes:
        inner_diameter: diameter of the pipe
        outer_diameter: diameter of the finished clamp
        height: height of the clamp
        tab_width: length of the mounting tabs (extending beyond outer_diameter)
        tab_depth: depth of the mounting tabs
        bolt_hole_diameter: diameter of the bolt hole through the tabs
        split_gap: distance bewween left and right halves
    """

    inner_diameter: float = 20.0
    outer_diameter: float = 30.0
    height: float = 10.0
    tab_width: float = 10.0
    tab_depth: float = 15.0
    bolt_hole_diameter: float = 4.0
    split_gap: float = 1.0

    def build(self) -> OpenSCADObject:
        """Build the bracket model.

        Returns:
            The SolidPython2 model representing the bracket with a mounting hole.
        """
        body = cylinder(h=self.height, r=self.outer_diameter / 2, center=True, _fn=128)
        hole = cylinder(h=self.height, r=self.inner_diameter / 2, center=True, _fn=128)
        tabs = cube(
            [self.outer_diameter + self.tab_width * 2, self.tab_depth, self.height],
            center=True,
        )
        bolt_hole = cylinder(
            h=self.tab_depth + 10, r=self.bolt_hole_diameter / 2, _fn=128, center=True
        )
        bolt_hole = bolt_hole.rotate(90, 0, 0)
        # x0 is where the mounting tab intersects the outer diameter
        x0 = math.sqrt((self.outer_diameter / 2) ** 2 - (self.tab_depth / 2) ** 2)
        # x1 is the right edge of the mounting tab
        x1 = self.outer_diameter / 2 + self.tab_width
        # bolt hole is halfway between x1 and x0
        bolt_offset = (x1 + x0) / 2
        bolt_hole_l = bolt_hole.translate([-bolt_offset, 0, 0])
        bolt_hole_r = bolt_hole.translate([bolt_offset, 0, 0])
        split_plane = cube(
            [self.outer_diameter + self.tab_width * 2, self.split_gap, self.height],
            center=True,
        )
        return (body + tabs) - (hole + bolt_hole_l + bolt_hole_r + split_plane)
