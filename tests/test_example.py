"""Tests for the ExampleBracket part."""

import shutil
from pathlib import Path

import pytest
from solid2.core.object_base import OpenSCADObject

from pystl.library.example import ExampleBracket


def test_build_returns_openscadobject() -> None:
    """build() with default params returns an OpenSCADObject instance."""
    part = ExampleBracket()
    result = part.build()
    assert isinstance(result, OpenSCADObject)


def test_build_custom_params() -> None:
    """build() with custom params returns an OpenSCADObject instance."""
    part = ExampleBracket(width=40.0, height=50.0, depth=8.0, hole_diameter=6.0)
    result = part.build()
    assert isinstance(result, OpenSCADObject)


@pytest.mark.skipif(shutil.which("openscad") is None, reason="openscad not in PATH")
def test_render_writes_files(tmp_path: Path) -> None:
    """render() writes both .scad and .stl files."""
    part = ExampleBracket()
    part.render(tmp_path)

    scad_file = tmp_path / "ExampleBracket.scad"
    stl_file = tmp_path / "ExampleBracket.stl"

    assert scad_file.exists(), f"{scad_file} was not created"
    assert stl_file.exists(), f"{stl_file} was not created"
    assert scad_file.stat().st_size > 0, "SCAD file is empty"
    assert stl_file.stat().st_size > 0, "STL file is empty"


def test_render_writes_scad(tmp_path: Path) -> None:
    """render() always writes a .scad file."""
    part = ExampleBracket()
    part.render(tmp_path)

    scad_file = tmp_path / "ExampleBracket.scad"
    assert scad_file.exists(), f"{scad_file} was not created"
    assert scad_file.stat().st_size > 0, "SCAD file is empty"
