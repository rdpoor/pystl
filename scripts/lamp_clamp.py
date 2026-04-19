"""General pipe clamp v1.0"""

import argparse
import math
from solid2 import cube, cylinder
from solid2.core.object_base import OpenSCADObject
from pystl.utils import write_model, setup_logging
import pystl.library.hex_nuts as hex_nuts


def _make_tab(
    outer_diameter: float,
    height: float,
    bolt_hole_diameter: float,
    tab_length: float,
    tab_width: float,
    tab_offset: float,
    tab_gap: float,
    is_front: bool,
    inset_nut_size: str,
    inset_side: str,
    inset_depth: float,
    fn: int,
):
    outer_radius = outer_diameter / 2
    end_cap_radius = height / 2
    mirror = 1 if is_front else -1

    # create a rectangular prism for the mounting tab.
    l1 = tab_length + outer_radius  # overall length
    l2 = l1 - end_cap_radius  # less endcap
    tab = cube([l2, tab_width, height], center=True)
    tab = tab.translate([mirror * l2 / 2, tab_offset, 0])
    end_cap = cylinder(h=tab_width, r=end_cap_radius, center=True, _fn=fn)
    end_cap = end_cap.rotate(90, 0, 0)
    end_cap = end_cap.translate([mirror * l2, tab_offset, 0])

    bolt_hole = cylinder(h=tab_width + 1, r=bolt_hole_diameter / 2, _fn=fn, center=True)
    bolt_hole = bolt_hole.rotate(90, 0, 0)
    bolt_hole = bolt_hole.translate([mirror * l2, tab_offset, 0])

    nut = hex_nuts.get(inset_nut_size)
    nut_inset_depth = inset_depth
    nut_inset = cylinder(h=nut_inset_depth * 2, r=nut.inset_radius, _fn=6, center=True)
    nut_inset = nut_inset.rotate(90, 0, 0)
    y_off = tab_width / 2 if inset_side == "left" else -tab_width / 2
    # need to fix y offset here...
    nut_inset = nut_inset.translate([mirror * l2, y_off + tab_offset, 0])

    split_plane = cube([l1, tab_gap, height + 1], center=True)
    split_plane = split_plane.translate([mirror * l1 / 2, tab_offset, 0])

    return (tab, end_cap, bolt_hole, nut_inset, split_plane)


YELNATS_FORK_UPPER_DIAMETER = 45
YELNATS_FORK_LOWER_DIAMETER = 48
CLAMP_THICKNESS = 5
CLAMP_HEIGHT = 20
MOUNTING_BOLT_DIAMETER = 4.2
TURN_SIGNAL_BOLT_DIAMETER = 10.1
FRONT_TAB_GAP = 3
REAR_TAB_GAP = 1

TAB_THICKNESS = 10
REAR_TAB_LENGTH = 14
LEFT_FRONT_TAB_OFFSET = 3
RIGHT_FRONT_TAB_OFFSET = -3
TOP_FRONT_TAB_LENGTH = 29
BOT_FRONT_TAB_LENGTH = 21


def build_clamp(is_top: bool = True, is_left: bool = True):
    front_tab_length = TOP_FRONT_TAB_LENGTH if is_top else BOT_FRONT_TAB_LENGTH
    front_bolt_diameter = (
        TURN_SIGNAL_BOLT_DIAMETER if is_top else MOUNTING_BOLT_DIAMETER
    )
    front_tab_offset = LEFT_FRONT_TAB_OFFSET if is_left else RIGHT_FRONT_TAB_OFFSET
    pass


def build_lamp_clamp(
    inner_diameter: float = YELNATS_FORK_UPPER_DIAMETER,
    outer_diameter: float = YELNATS_FORK_UPPER_DIAMETER + CLAMP_THICKNESS * 2,
    height: float = CLAMP_HEIGHT,
    front_tab_length: float = 22,
    front_tab_width: float = 10,
    front_tab_offset: float = 3,
    front_tab_gap: float = 3.0,  # must match turn_signal_bolt_diameter in lamp_frame
    front_bolt_hole_diameter: float = TURN_SIGNAL_BOLT_DIAMETER,
    rear_tab_length: float = 14,
    rear_tab_width: float = 10,
    rear_tab_offset: float = 0,
    rear_tab_gap: float = 1.0,
    rear_bolt_hole_diameter: float = 4.2,
    inset_nut_size: str = "M4",
    inset_side: str = "left",
    inset_depth: float = 1.0,
    fn: int = 128,
) -> OpenSCADObject:
    """Clamps to attach headlamp to front fork.

    Attributes:
        inner_diameter: diameter of the pipe
        outer_diameter: diameter of the finished clamp
        height: height of the clamp
        left_tab_length: length of front mounting tab extending beyond
            outer_diameter
        left_tab_width: width of the front mounting tab
        right_tab_length: length of rear mounting tab extending beyond
            outer_diameter
        right_tab_width: width of the rear mounting tab
        bolt_hole_diameter: diameter of the bolt hole through the tabs
        split_gap: distance bewween left and right halves
    """
    r = outer_diameter / 2  # radius of outer diameter
    outer = cylinder(h=height, r=r, center=True, _fn=128)
    inner = cylinder(h=height + 1, r=inner_diameter / 2, center=True, _fn=128)

    # create a rectangular prism for the mounting tab.
    # it has an end cap of radius height/2, so we shorten the length by that
    # amount, shift x to the left
    left_tab = cube([left_tab_length - height / 2, left_tab_width, height], center=True)
    x1 = math.sqrt(r**2 - (left_tab_width / 2) ** 2)
    x2 = x1 + (left_tab_length - height / 2) / 2
    x3 = x1 + left_tab_length - height / 2
    left_tab = left_tab.translate([-x2, 0, 0])
    left_end_cap = cylinder(h=left_tab_width, r=height / 2, center=True, _fn=32)
    left_end_cap = left_end_cap.rotate(90, 0, 0)
    left_end_cap = left_end_cap.translate([-x3, 0, 0])

    left_bolt_hole = cylinder(
        h=left_tab_width + 1, r=bolt_hole_diameter / 2, _fn=128, center=True
    )
    left_bolt_hole = left_bolt_hole.rotate(90, 0, 0)
    left_bolt_hole = left_bolt_hole.translate([-x3, 0, 0])

    # create a rectangular prism for the mounting tab, shift x to the right
    right_tab = cube(
        [right_tab_length - height / 2, right_tab_width, height], center=True
    )
    x1 = math.sqrt(r**2 - (right_tab_width / 2) ** 2)
    x2 = x1 + (right_tab_length - height / 2) / 2
    x3 = x1 + right_tab_length - height / 2
    right_tab = right_tab.translate([x2, 0, 0])
    right_end_cap = cylinder(h=right_tab_width, r=height / 2, center=True, _fn=32)
    right_end_cap = right_end_cap.rotate(90, 0, 0)
    right_end_cap = right_end_cap.translate([x3, 0, 0])

    right_bolt_hole = cylinder(
        h=right_tab_width + 1, r=bolt_hole_diameter / 2, _fn=128, center=True
    )
    right_bolt_hole = right_bolt_hole.rotate(90, 0, 0)
    right_bolt_hole = right_bolt_hole.translate([x3, 0, 0])

    # create a thin rectagular prism to split the entire assembly
    split_plane = cube(
        [
            outer_diameter + 2 * max(left_tab_length, right_tab_length),
            split_gap,
            height + 1,
        ],
        center=True,
    )
    model = (outer + left_tab + left_end_cap + right_tab + right_end_cap) - (
        inner + split_plane + left_bolt_hole + right_bolt_hole
    )

    return model


def main() -> None:
    """render LampSidePanel."""
    lamp_clamp = build_lamp_clamp()
    write_model(lamp_clamp, "output/lamp_clamp_01")


if __name__ == "__main__":
    setup_logging()
    main()
