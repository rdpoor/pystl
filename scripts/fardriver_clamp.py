#!/usr/bin/env python3
"""
Clamp (1 of 2) to hold Fardriver Controller to top tube of MX500 emoto
"""
import math

from solid2 import linear_extrude, polygon, cylinder
from solid2.core.object_base import OpenSCADObject
from pystl.py_stl_geometry import PyStlGeometry
from pystl.py_stl_part import PyStlPart
from pystl.utils import write_model, setup_logging

def build_fardriver_clamp() -> PyStlGeometry:
    m8_clearance_diameter = 9
    m8_spacing = 105
    m4_clearance_diameter = 5

    clamp_width = 117.9
    clamp_thickness = 10
    clamp_depth = 20     # extrusion in z

    top_tube_width = 40.2
    top_tube_height = 25.4

    fn=128

    # create 2d outline, extrude to 3d
    clamp_2d = polygon(
        [
            [-clamp_width/2, 0],
            [-clamp_width/2, clamp_thickness],
            [(-clamp_width/2)+15, clamp_thickness],
            [(-top_tube_width/2)-5, top_tube_height+5],
            [(top_tube_width/2)+5, top_tube_height+5],
            [(clamp_width/2)-15, clamp_thickness],
            [clamp_width/2, clamp_thickness],
            [clamp_width/2, 0],
            [top_tube_width/2, 0],
            [top_tube_width/2, top_tube_height],
            [-top_tube_width/2, top_tube_height],
            [-top_tube_width/2, 0],
            [-clamp_width/2, 0],
        ]
    )
    clamp_3d = clamp_2d.linear_extrude(clamp_depth, center=True)
    clamp_3d = clamp_3d.rotate(90, 0, 0)
    positive = clamp_3d

    # add bolt holes
    m4_hole = cylinder(
            h=clamp_thickness + PyStlPart.CUT_CLEARANCE,
            d=m4_clearance_diameter,
            center=True,
            _fn=fn,
        )
    m8_hole = cylinder(
            h=clamp_thickness + PyStlPart.CUT_CLEARANCE,
            d=m8_clearance_diameter,
            center=True,
            _fn=fn,
        )
    m4_up = m4_hole.translate([0, 0, top_tube_height + 5])
    m8_left = m8_hole.translate([-m8_spacing/2, 0, clamp_thickness/2])
    m8_right = m8_hole.translate([m8_spacing/2, 0, clamp_thickness/2])

    negative = m4_up + m8_left + m8_right
    return PyStlGeometry(positive=positive, negative=negative)

    # bolt_hole = circle(r=bolt_diameter/2, _fn=64)
    # top_hole = bolt_hole.translate([-25, 0, 0])
    # bot_hole = bolt_hole.translate([25, 0, 0])
    # retainer2d = (plate) - (top_hole + bot_hole)

    # m4_nut_width = 7.0
    # nut_insert_depth = 1.0
    # nut_insert2d = circle(r=nut_width_to_radius(m4_nut_width), _fn=6)
    # nut_insert3d = nut_insert2d.linear_extrude(nut_insert_depth+1)
    # top_insert = nut_insert3d.translate([-25, 0, retainer_thickness-nut_insert_depth])
    # bot_insert = nut_insert3d.translate([25, 0, retainer_thickness-nut_insert_depth])

    # return retainer2d.linear_extrude(retainer_thickness) - (top_insert + bot_insert)

def main() -> None:
    """render LampSidePanel."""
    setup_logging()
    clamp = build_fardriver_clamp()
    write_model(clamp.combined(), "output/fardriver_clamp")


if __name__ == "__main__":
    main()
