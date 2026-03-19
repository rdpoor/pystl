#!/usr/bin/env python3
"""Boilerplate script for a new pystl part.

Copy this file to scripts/<my_part>.py and customize:
  1. Rename MyCustomPart (and update the argparse description).
  2. Add @dataclass fields for your parameters.
  3. Implement build() using library parts from pystl.library and/or solid2 primitives.
  4. Extend main() with extra argparse flags if needed.

Run:
    uv run python scripts/<my_part>.py [--param val ...] [--outdir dir]
"""

from dataclasses import dataclass

from solid2 import cube
from solid2.core.object_base import OpenSCADObject

from pystl import cli
from pystl.py_stl_base import PyStlPart


@dataclass
class MyCustomPart(PyStlPart):
    """A custom part. Replace this docstring and implement build().

    Attributes:
        width: Side length of the example cube in mm.
    """

    width: float = 30.0

    def build(self) -> OpenSCADObject:
        """Build and return the OpenSCAD model for this part.

        Returns:
            The SolidPython2 model object.
        """
        return cube([self.width, self.width, self.width])


def main() -> None:
    """Parse arguments and render MyCustomPart."""
    cli.build_and_render(MyCustomPart)


if __name__ == "__main__":
    main()
