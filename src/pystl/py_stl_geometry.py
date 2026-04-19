"""Positive/negative geometry pair for SolidPython2 models."""

from __future__ import annotations

from dataclasses import dataclass

from solid2 import cube, linear_extrude as _linear_extrude
from solid2.core.object_base import OpenSCADObject

_empty_export: OpenSCADObject | None = None


def _trivial_empty_solid() -> OpenSCADObject:
    """Minimal solid used only when :meth:`PyStlGeometry.combined` must return a model with no material."""
    global _empty_export
    if _empty_export is None:
        _empty_export = cube([1e-9, 1e-9, 1e-9], center=True)
    return _empty_export


@dataclass(frozen=True, slots=True)
class PyStlGeometry:
    """Solid fill (positive) and cutters (negative) before final ``difference``.

    Attributes:
        positive: Material to keep, or ``None`` when there is no fill geometry.
        negative: Geometry to subtract, or ``None`` when there are no cutters.
    """

    positive: OpenSCADObject | None
    negative: OpenSCADObject | None

    def __add__(self, other):
        """Support geometry1 + geometry2 syntax."""
        if not isinstance(other, PyStlGeometry):
            return NotImplemented
        # Return a new instance that accumulates both geometries
        return self.accumulate(other)

    def __radd__(self, other):
        """Support sum([geo1, geo2, geo3]) which starts with 0."""
        if other == 0:  # sum() starts with integer 0
            return self
        return self.__add__(other)\

    def accumulate(self, other: PyStlGeometry) -> PyStlGeometry:
        if self.positive is None:
            positive = other.positive
        elif other.positive is None:
            positive = self.positive
        else:
            positive = self.positive + other.positive

        if self.negative is None:
            negative = other.negative
        elif other.negative is None:
            negative = self.negative
        else:
            negative = self.negative + other.negative

        return PyStlGeometry(positive=positive, negative=negative)

    def translate(self, vector: list[float]) -> PyStlGeometry:
        return PyStlGeometry(
            positive=self.positive.translate(vector) if self.positive is not None else None,
            negative=self.negative.translate(vector) if self.negative is not None else None,
        )

    def rotate(self, x: float, y: float, z: float) -> PyStlGeometry:
        return PyStlGeometry(
            positive=self.positive.rotate([x, y, z]) if self.positive is not None else None,
            negative=self.negative.rotate([x, y, z]) if self.negative is not None else None,
        )

    def linear_extrude(self, height: float) -> PyStlGeometry:
        return PyStlGeometry(
            positive=_linear_extrude(height)(self.positive) if self.positive is not None else None,
            negative=_linear_extrude(height)(self.negative) if self.negative is not None else None,
        )

    def combined(self) -> OpenSCADObject:
        """Return ``positive - negative``, treating ``None`` as an empty side."""
        if self.positive is None and self.negative is None:
            return _trivial_empty_solid()
        if self.positive is None:
            return _trivial_empty_solid()
        if self.negative is None:
            return self.positive
        return self.positive - self.negative
