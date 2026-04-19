#!/usr/bin/env python3
"""
Side panels that hold the lamp against the front of the lamp frame.
"""

import math

from solid2 import circle, linear_extrude, polygon
from solid2.core.object_base import OpenSCADObject
from pystl.utils import write_model, setup_logging


def nut_width_to_radius(s):
    """Given the distance bewtween flats of a hex nut, return the radius of the
    inscribed circle (distance between verteces)
    """
    return s / math.sqrt(3)


def build_lamp_retainer() -> OpenSCADObject:
    bolt_diameter = 4.2
    retainer_thickness = 3.0

    plate = polygon(
        [
            [-33, -9.75],
            [-33, 9.75],
            [-9, 9.75],
            [-9, 6.25],
            [9, 6.25],
            [9, 9.75],
            [33, 9.75],
            [33, -9.75],
            [-33, -9.75],
        ]
    )
    bolt_hole = circle(r=bolt_diameter / 2, _fn=64)
    top_hole = bolt_hole.translate([-25, -1, 0])
    bot_hole = bolt_hole.translate([25, -1, 0])
    retainer2d = (plate) - (top_hole + bot_hole)

    m4_nut_width = 7.0
    nut_insert_depth = 1.5
    nut_insert2d = circle(r=nut_width_to_radius(m4_nut_width), _fn=6)
    nut_insert3d = nut_insert2d.linear_extrude(nut_insert_depth + 1)
    top_insert = nut_insert3d.translate([-25, -1, retainer_thickness - nut_insert_depth])
    bot_insert = nut_insert3d.translate([25, -1, retainer_thickness - nut_insert_depth])

    return retainer2d.linear_extrude(retainer_thickness) - (top_insert + bot_insert)


def main() -> None:
    """render LampSidePanel."""
    setup_logging()
    retainer = build_lamp_retainer()
    write_model(retainer, "output/lamp_retainer_02")


if __name__ == "__main__":
    main()
