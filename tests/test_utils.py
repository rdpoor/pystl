"""Tests for geometry utilities."""

from solid2 import cube
from solid2.core.object_base import OpenSCADObject

from pystl.utils import split_at_y


def test_split_at_y_returns_two_openscadobjects() -> None:
    obj = cube([10, 10, 10]).translate([-5, -5, -5])
    neg, pos = split_at_y(obj)
    assert isinstance(neg, OpenSCADObject)
    assert isinstance(pos, OpenSCADObject)


def test_split_at_y_produces_valid_scad() -> None:
    obj = cube([10, 10, 10]).translate([-5, -5, -5])
    neg, pos = split_at_y(obj)
    assert neg.as_scad()
    assert pos.as_scad()


def test_split_at_y_scad_contains_intersection() -> None:
    obj = cube([10, 10, 10]).translate([-5, -5, -5])
    neg, pos = split_at_y(obj)
    assert "intersection" in neg.as_scad()
    assert "intersection" in pos.as_scad()
