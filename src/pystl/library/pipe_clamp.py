"""Parametric split pipe clamp built from a ring and tab sub-parts."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from solid2 import cube, cylinder

from pystl.library.py_stl_inset import PyStlInset
from pystl.py_stl_geometry import PyStlGeometry
from pystl.py_stl_part import PyStlPart


@dataclass
class PipeClampTab(PyStlPart):
    """One mounting tab expressed as its own positive/negative pair.

    A tab is a rectangular body with a cylindrical end cap containing a
    bolt hole and a split gap. It is positioned relative to the pipe
    center by :class:`PipeClamp` during assembly.

    Attributes:
        height: Tab thickness along the pipe axis (mm); usually inherited
            from the parent :class:`PipeClamp` so the tab flush with the
            ring.
        width: Extent of the tab across the bolt axis (mm).
        length: Distance from the pipe center to the bolt hole (mm).
        offset: Translation along Y applied before rotation (mm).
        angle: Rotation about Z placing the tab around the clamp (deg).
        drill_diameter: Diameter of the bolt through-hole (mm).
        split_gap_width: Width of the clamp split gap cut (mm).
        front_inset: Optional inset feature on the -Y face of the tab.
        rear_inset: Optional inset feature on the +Y face of the tab.
        fn: Fragment count for curved primitives.
    """

    height: float = 10.0
    width: float = 10.0   # width across tab (drill hole length)
    length: float = 30.0  # distance from pipe center to drill hole
    angle: float = 0
    offset: float = 0
    drill_diameter: float = 4
    split_gap_width: float = 1
    front_inset: PyStlInset | None = None
    rear_inset: PyStlInset | None = None
    fn: int = 64

    def build(self) -> PyStlGeometry:
        """Construct the tab geometry, including positive solid and cutouts.

        This method assembles a composite ``PyStlGeometry`` object
        representing a mechanical tab that attaches to an outer clamp
        shell. The geometry is defined as a combination of:

        - Positive volume:
            * A rectangular tab body extending along ``self.length``.
            * A cylindrical end cap at the distal end of the tab.

        - Negative volume (subtractive features):
            * A through-hole for a drill/bolt.
            * A split gap through the tab body.
            * Clearance-expanded cut regions for robust boolean ops.

        Construction steps:
            1. Create the cylindrical end cap and associated drill hole.
            2. Position and orient this end feature at the tab tip.
            3. Create the rectangular tab body and central split gap.
            4. Combine body and end features into a single geometry.
            5. Apply optional translation (``self.offset``) along Y.
            6. Apply optional rotation (``self.angle``) about Z.

        Notes:
            - All primitives are centered before transformation.
            - ``CUT_CLEARANCE`` ensures robust boolean operations.
            - Final geometry is returned with accumulated transforms.

        Returns:
            PyStlGeometry: Positive and negative volumes suitable for
                downstream boolean evaluation or STL export.
        """
        end_cap = cylinder(
            h=self.width, d=self.height, center=True, _fn=self.fn
        )
        drill_hole = cylinder(
            h=self.width + self.CUT_CLEARANCE,
            d=self.drill_diameter,
            center=True,
            _fn=self.fn,
        )
        end_gap = cube(
            [
                self.height + self.CUT_CLEARANCE,
                self.height + self.CUT_CLEARANCE,
                self.split_gap_width,
            ],
            center=True,
        )
        g1 = (
            PyStlGeometry(
                positive=end_cap,
                negative=drill_hole + end_gap,
            )
            .rotate(90, 0, 0)
            .translate([self.length, 0, 0])
        )

        tab_body = cube([self.length, self.width, self.height], center=True)
        tab_gap = cube(
            [
                self.length + self.height / 2,
                self.split_gap_width,
                self.height + self.CUT_CLEARANCE,
            ],
            center=True,
        )
        g2 = (
            PyStlGeometry(positive=tab_body, negative=tab_gap)
            .translate([self.length / 2, 0, 0])
        )

        g3 = g2.accumulate(g1)

        # At this point, g3 has angle=0 and no offset and no insets

        # add insets.
        if self.front_inset is not None:
            gi = (
                self.front_inset.build()
                .rotate(90, 0, 0)
                .translate([self.length, -self.width / 2, 0])
            )
            g3 = g3.accumulate(gi)
        if self.rear_inset is not None:
            gi = (
                self.rear_inset.build()
                .rotate(-90, 0, 0)
                .translate([self.length, self.width / 2, 0])
            )
            g3 = g3.accumulate(gi)

        # offset along Y axis
        if self.offset != 0:
            g3 = g3.translate([0, self.offset, 0])

        # rotate into position
        if self.angle != 0:
            g3 = g3.rotate(0, 0, self.angle)

        return g3


@dataclass
class PipeClamp(PyStlPart):
    """Pipe clamp ring plus zero or more :class:`PipeClampTab` instances.

    Attributes:
        inner_diameter: Bore for the pipe (mm).
        wall_thickness: Radial thickness of the clamp body (mm).
        height: Extrusion height along the pipe axis (mm).
        tabs: Sub-parts merged into the final clamp; each contributes
            its own ``PyStlGeometry`` in :meth:`build`.
        fn: Fragment count for curved primitives (ring and tabs).
    """

    inner_diameter: float = 20.0
    wall_thickness: float = 5.0
    height: float = 10.0
    tabs: list[PipeClampTab] = field(default_factory=list)
    fn: int = 64

    @property
    def outer_diameter(self) -> float:
        """Inside bore plus twice the wall."""
        return self.inner_diameter + 2.0 * self.wall_thickness

    def add_tab(self, **kwargs: Any) -> PipeClamp:
        """Append a tab; ``height`` is inherited so the tab matches the ring."""
        self.tabs.append(PipeClampTab(height=self.height, **kwargs))
        return self

    def build(self) -> PyStlGeometry:
        """Combine ring and tabs into one positive/negative pair.

        Inner bore uses ``height + CUT_CLEARANCE`` so the cut clears
        the ring cleanly in CSG.
        """
        positive = cylinder(
            h=self.height,
            d=self.outer_diameter,
            center=True,
            _fn=self.fn,
        )
        negative = cylinder(
            h=self.height + self.CUT_CLEARANCE,
            d=self.inner_diameter,
            center=True,
            _fn=self.fn,
        )

        geometry = PyStlGeometry(positive=positive, negative=negative)
        for tab in self.tabs:
            geometry = geometry.accumulate(tab.build())

        return geometry
