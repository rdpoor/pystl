"""Clamp for left or right turn signal, mounted on front fork"""

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
    inset_side: str,
    inset_depth: float,
    fn: int
    ):
    outer_radius = outer_diameter / 2
    end_cap_radius = height/2
    mirror = -1 if is_front else 1

    # create a rectangular prism for the mounting tab.
    l1 = tab_length + outer_radius     # overall length
    l2 = l1 - end_cap_radius           # less endcap
    tab = cube([l2, tab_width, height], center=True)
    tab = tab.translate([mirror * l2/2, tab_offset, 0])
    end_cap = cylinder(
        h=tab_width, r=end_cap_radius, center=True, _fn=fn
    )
    end_cap = end_cap.rotate(90, 0, 0)
    end_cap = end_cap.translate([mirror * l2, tab_offset, 0])

    bolt_hole = cylinder(
        h=tab_width + 1, r=bolt_hole_diameter / 2, _fn=fn, center=True
    )
    bolt_hole = bolt_hole.rotate(90, 0, 0)
    bolt_hole = bolt_hole.translate([mirror * l2, tab_offset, 0])

    nut = hex_nuts.get('M4')
    nut_inset_depth = inset_depth
    nut_inset = cylinder(
        h=nut_inset_depth * 2, r=nut.inset_radius, _fn=6, center=True
    )
    nut_inset = nut_inset.rotate(90, 0, 0)
    y_off = tab_width/2 if inset_side == 'left' else -tab_width/2
    # need to fix y offset here...
    nut_inset = nut_inset.translate([mirror * l2, y_off + tab_offset, 0])

    split_plane = cube([l1, tab_gap, height+1], center=True)
    split_plane = split_plane.translate([mirror * l1/2, tab_offset, 0])

    return (tab, end_cap, bolt_hole, nut_inset, split_plane)

def build_turn_signal_clamp(
    inner_diameter: float = 45,
    outer_diameter: float = 53,
    height: float = 15,
    front_tab_length: float = 17,
    front_tab_width: float = 10,
    front_tab_offset: float = 0,
    front_tab_gap: float = 0.5,
    front_bolt_hole_diameter: float = 10,
    rear_tab_length: float = 12,
    rear_tab_width: float = 10,
    rear_tab_offset: float = 0,
    rear_tab_gap: float = 0.5,
    rear_bolt_hole_diameter: float = 4.2,
    inset_side: str = 'left',
    inset_depth: float = 1.0,
    fn: int = 128,
) -> OpenSCADObject:
    """Clamps to attach headlamp to front fork, where front and rear tabs can
    be offset from the center.

    Attributes:
        inner_diameter: diameter of the pipe
        outer_diameter: diameter of the finished clamp
        height: height of the clamp
        bolt_hole_diameter: diameter of the bolt hole through the tabs
        front_tab_length: length of front mounting tab extending beyond
            outer_diameter
        front_tab_width: width of the front mounting tab
        front_tab_offset: offset from center
        front_tab_gap: width of the split betwen left and right halves
        rear_tab_length: length of rear mounting tab extending beyond
            outer_diameter
        rear_tab_width: width of the rear mounting tab
        rear_tab_offset: offset from center
        rear_tab_gap: width of the split between left and right halves
        inset_side: left or right (determines side of nut inset)
        fn: number of polygon sides for cylinders
    """
    outer = cylinder(h=height, r=outer_diameter / 2, center=True, _fn=fn)
    inner = cylinder(
        h=height + 1, r=inner_diameter / 2, center=True, _fn=fn
    )

    front_tab, front_end_cap, front_bolt_hole, front_nut_inset, front_split_plane = _make_tab(
        outer_diameter,
        height,
        front_bolt_hole_diameter,
        front_tab_length,
        front_tab_width,
        front_tab_offset,
        front_tab_gap,
        True,
        inset_side,
        inset_depth,
        fn)

    rear_tab, rear_end_cap, rear_bolt_hole, rear_nut_inset, rear_split_plane = _make_tab(
        outer_diameter,
        height,
        rear_bolt_hole_diameter,
        rear_tab_length,
        rear_tab_width,
        rear_tab_offset,
        rear_tab_gap,
        False,
        inset_side,
        inset_depth,
        fn)

    model = (
        (outer + front_tab + front_end_cap + rear_tab + rear_end_cap)
        - (inner + front_split_plane + front_bolt_hole + front_nut_inset + rear_split_plane + rear_bolt_hole + rear_nut_inset)
    )

    return model

def main() -> None:
    """render offset lamp clamp."""
    tab_length = 24 + 4
    lower_tab_length = 24 - 4
    setup_logging()
    parser = argparse.ArgumentParser(
        description="Render clamps to hold turn signals to front fork."
    )
    parser.add_argument(
        '--fork-side',
        required=True,
        choices=['left', 'right'],
        help="which fork tube the clamp goes on"
    )
    args = parser.parse_args()
    model = build_turn_signal_clamp(
        inset_side=args.fork_side,
        inset_depth=2,
        )
    write_model(model, f"output/{args.fork_side}_turn_signal_clamp_01")

if __name__ == "__main__":
    main()
