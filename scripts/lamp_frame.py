#!/usr/bin/env python3
"""
Create an escutcheon by merging a FilletedFrame as a faceplate and another
FilletedFrame as the sidewalls plus a pair of mounting ears.

Run:
    uv run python scripts/lamp_frame.py [--param val ...] [--outdir dir]
"""

from dataclasses import dataclass
import numpy as np
import math

from solid2 import circle, linear_extrude, polygon

from pystl.library.filleted_rect import FilletedFrame
from pystl.py_stl_geometry import PyStlGeometry
from pystl.py_stl_part import PyStlPart
from pystl.utils import setup_logging, write_model

setup_logging()

def slotted_arc(x_org, y_org, start_deg, end_deg, radius, slot_width, fn=128):
    """
    Create a 2D slotted arc.
    Arguments:
        x_org: x origin of the arc
        y_org: y origin of the arc
        start_deg: starting angle of arc (in degrees [0..360])
        end_deg: ending angle of arc (in degrees [0..360])
        radius: distance from origin to center of the arc's slot
        slot_width: width of the slot
        fn: number of polygon steps to create the arc
    """

    def _dtor(degree):
        return degree * math.pi / 180.0

    k = max(3, fn)

    # Create linearly spaced angles from start to end (inclusive)
    thetas = [_dtor(degree) for degree in np.linspace(start_deg, end_deg, k)]

    r0 = radius - slot_width / 2.0
    r1 = radius + slot_width / 2.0

    inner = [
        [x_org + r0 * math.cos(theta), y_org + r0 * math.sin(theta)]
        for theta in thetas
    ]
    outer = [
        [x_org + r1 * math.cos(theta), y_org + r1 * math.sin(theta)]
        for theta in reversed(thetas)
    ]

    # drop a circle at either end of the arc to make a rounded slot
    end_cap = circle(r=slot_width / 2, _fn=fn)
    e0 = end_cap.translate(
        [
            x_org + radius * math.cos(thetas[0]),
            y_org + radius * math.sin(thetas[0]),
            0
        ]
    )
    e1 = end_cap.translate(
        [
            x_org + radius * math.cos(thetas[-1]),
            y_org + radius * math.sin(thetas[-1]),
            0,
        ]
    )
    return polygon(inner + outer) + e0 + e1


TURN_SIGNAL_BOLT_DIAMETER = 10.3


def build_mounting_ear(ear_thickness: float = 3.0) -> PyStlPart:

    # Retaining bolts hold lamp_retainer.py (a separate part)
    retaining_bolt_diameter = 4.3
    retaining_bolt_spacing = 50
    retaining_bolt_hole = circle(
        r=retaining_bolt_diameter / 2,
        _fn=128,
    )
    upper_retaining_bolt = retaining_bolt_hole.translate(
        [retaining_bolt_spacing / 2, 6, 0]
    )
    lower_retaining_bolt = retaining_bolt_hole.translate(
        [-retaining_bolt_spacing / 2, 6, 0]
    )

    mounting_bolt_diameter = TURN_SIGNAL_BOLT_DIAMETER
    mounting_bolt_hole = circle(
        r=mounting_bolt_diameter / 2,
        _fn=128,
    )
    # upper mounting bolt is the pivot point and doubles as turn signal holder.
    upper_mounting_bolt = mounting_bolt_hole.translate([-15, 30, 0])
    # lower mounting slot is an arc to allow vertical adjustment.
    lower_mounting_slot = slotted_arc(
        0, 0, -14, +14, 30, retaining_bolt_diameter, fn=128
    )
    lower_mounting_slot = lower_mounting_slot.translate([-15, 30, 0])

    plate = polygon(
        [
            [-66 / 2, 0],
            [-66 / 2, 30],
            [-(66 / 2) + 11, 41],
            [(66 / 2) - 11, 41],
            [66 / 2, 30],
            [66 / 2, 0],
            [-66 / 2, 0],
        ],
    )
    holes = (
        upper_retaining_bolt
        + lower_retaining_bolt
        + upper_mounting_bolt
        + lower_mounting_slot
        )

    # Up to this point, plate and holes are 2D.  Extrude into 3D
    plate3D = plate.linear_extrude(ear_thickness)
    holes3D = holes.linear_extrude(ear_thickness + PyStlPart.CUT_CLEARANCE)
    return PyStlGeometry(
        positive = plate3D.translate([0, 0, -ear_thickness/2]),
        negative = holes3D.translate(
            [
                0,
                0,
                -(ear_thickness + PyStlPart.CUT_CLEARANCE)/2
            ]
        )
    )

@dataclass
class LampFrame01(PyStlPart):
    """
    Assemble a frame for the e-moto headlamp, comprising:
    - faceplate - a filleted escutcheon that's frontmost
    - sidewalls - a deep filleted escutcheon that surrounds the lamp assembly
    - mounting_ears - a polygon with holes to hold the captive side panels

    Attributes:
        lamp_width: width of the lamp housing
        lamp_length: height of the housing
        lamp_radius: fillet radius of the lamp housing corner
        cutout_width: width of the faceplate cutout rectangle
        cutout_length: height of the faceplate cutout rectangle
        cutout_radius: fillet radius of the faceplate cutout rectangle
        faceplate_thickness: thickness of the faceplate
        sidewall_thickness: thickness of the sidewall
        sidewall_depth: depth of the sidewall
    """

    lamp_width: float = 169.16 + 0.5
    lamp_length: float = 107.5 + 0.5
    lamp_radius: float = 15

    sidewall_thickness = 3.0
    sidewall_depth: float = 17.0

    escutcheon_thickness = sidewall_thickness + 3.0
    faceplate_depth = 3.0
    faceplate_thickness = 6.0
    # sidewall inner dimensions = lamp dimensions (snug fit)
    # sidewall outer dimensions = inner dimensions + sidewall_thickness


    def build(self) -> PyStlGeometry:
        frame_outer_width = self.lamp_width + 2 * self.sidewall_thickness
        frame_outer_length = self.lamp_length + 2 * self.sidewall_thickness
        frame_outer_radius = self.lamp_radius + self.sidewall_thickness

        faceplate = FilletedFrame(
            outer_width=frame_outer_width,
            outer_height=frame_outer_length,
            outer_radius=frame_outer_radius,
            frame_thickness = self.escutcheon_thickness,
            depth=self.faceplate_thickness,
        ).build()

        sidewalls = FilletedFrame(
            outer_width=frame_outer_width,
            outer_height=frame_outer_length,
            outer_radius=frame_outer_radius,
            frame_thickness = self.sidewall_thickness,
            depth=self.sidewall_depth,
        ).build().translate([0, 0, self.faceplate_depth])

        mounting_ear = build_mounting_ear(self.sidewall_thickness)
        mounting_ear = mounting_ear.rotate(90, 00, 90)
        # translate to form left and right mounting ears
        left_mounting_ear = mounting_ear.translate([
            -self.lamp_width/2 - self.sidewall_thickness/2,
            0,
            self.faceplate_depth + self.sidewall_depth])
        right_mounting_ear = mounting_ear.translate([
            self.lamp_width/2 + self.sidewall_thickness/2,
            0,
            self.faceplate_depth + self.sidewall_depth])
        return faceplate + sidewalls + left_mounting_ear + right_mounting_ear

def main() -> None:
    """Parse arguments and render LampFrame."""
    write_model(LampFrame01().build().combined(), "output/lamp_frame")

if __name__ == "__main__":
    main()
