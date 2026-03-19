#!/usr/bin/env python3
"""
Side panels to bolt into headlamp escutcheon 

Run:
    uv run python scripts/lamp_side_panel.py [--param val ...] [--outdir dir]
"""

from dataclasses import dataclass

from solid2 import cube, cylinder
from solid2.core.object_base import OpenSCADObject

from pystl import cli
from pystl.library.filleted_rect import FilletedFrame
from pystl.py_stl_base import PyStlPart


@dataclass
class LampSidePanel(PyStlPart):
    """Create a side plate to hold headlamp against escutcheon
    """

    part_width: float = 66.0
    part_height: float = 14.0
    part_thickness: float = 3.0
    notch_width: float = 18.0
    notch_height: float = 4.0
    bolt_diameter: float = 4.5

    def build(self) -> OpenSCADObject:

        bolt_hole = cylinder(
            h=self.part_thickness + 1, 
            r=self.bolt_diameter / 2, 
            _fn=128, 
            center=True
        )
        unnotched_width = (self.part_width - self.notch_width)/2
        unnotched_center = unnotched_width/2.0
        bolt_x_offset = self.notch_width / 2 + unnotched_center

        left_bolt = bolt_hole.translate([bolt_x_offset, 0, 0])
        right_bolt = bolt_hole.translate([-bolt_x_offset, 0, 0])
        plate = cube(
            [self.part_width, self.part_height, self.part_thickness],
            center=True,
        )
        notch = cube(
            [self.notch_width, self.notch_height, self.part_thickness + 1],
            center=True,
        )
        notch = notch.translate([0, self.part_height/2 - self.notch_height/2, 0])

        return plate - (notch + left_bolt + right_bolt)


def main() -> None:
    """render LampSidePanel."""
    cli.build_and_render(LampSidePanel)


if __name__ == "__main__":
    main()
