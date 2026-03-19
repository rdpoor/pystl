#!/usr/bin/env python3
"""
Create an escutcheon by merging a FilletedFrame as a faceplate and another
FilletedFrame as the sidewalls.

Run:
    uv run python scripts/filleted_escutcheon.py [--param val ...] [--outdir dir]
"""

from dataclasses import dataclass

from solid2.core.object_base import OpenSCADObject

from pystl import cli
from pystl.library.filleted_rect import FilletedFrame
from pystl.py_stl_base import PyStlPart


@dataclass
class FilletedEscutcheon(PyStlPart):
    """Merge a FilletedFrame as the faceplate with another FilletedFrame as the
    sidewalls.

    Attributes:
        part_width: width of the part
        part_height: height of the part
        part_radius: fillet radius of the part corner
        cutout_width: width of the cutout rectangle
        cutout_height: height of the cutout rectangle
        cutout_radius: fillet radius of the cutout rectangle
        faceplate_thickness: thickness of the faceplate
        sidewall_thickness: thickness of the sidewall
        sidewall_depth: depth of the sidewall
    """

    part_width: float = 169.16 + 1
    part_height: float = 107.5 + 1
    part_radius: float = 16.5
    cutout_width: float = 160.5
    cutout_height: float = 100.5
    cutout_radius: float = 11.5
    faceplate_thickness: float = 3.0
    sidewall_thickness: float = 3.0
    sidewall_depth: float = 20.0

    def build(self) -> OpenSCADObject:
        faceplate_outer_width = self.part_width + 2 * self.sidewall_thickness
        faceplate_outer_height = self.part_height + 2 * self.sidewall_thickness
        faceplate_outer_radius = self.part_radius + self.sidewall_thickness

        faceplate = FilletedFrame(
            outer_width=faceplate_outer_width,
            outer_height=faceplate_outer_height,
            outer_radius=faceplate_outer_radius,
            inner_width=self.cutout_width,
            inner_height=self.cutout_height,
            inner_radius=self.cutout_radius,
            depth=self.faceplate_thickness,
        ).build()
        sidewalls = FilletedFrame(
            outer_width=faceplate_outer_width,
            outer_height=faceplate_outer_height,
            outer_radius=faceplate_outer_radius,
            inner_width=self.part_width,
            inner_height=self.part_height,
            inner_radius=self.part_radius,
            depth=self.sidewall_depth,
        ).build()
        return faceplate + sidewalls


def main() -> None:
    """Parse arguments and render FilletedEscutcheon."""
    cli.build_and_render(FilletedEscutcheon)


if __name__ == "__main__":
    main()
