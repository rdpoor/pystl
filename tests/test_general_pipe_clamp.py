"""Tests for GeneralPipeClamp."""

from pathlib import Path

from solid2.core.object_base import OpenSCADObject

from pystl.library.general_pipe_clamp import GeneralPipeClamp


def test_build_defaults() -> None:
    """build() with default params returns an OpenSCADObject."""
    result = GeneralPipeClamp().build()
    assert isinstance(result, OpenSCADObject)


def test_build_custom_params() -> None:
    """build() with overridden params returns an OpenSCADObject."""
    result = GeneralPipeClamp(inner_diameter=25.0, tab_depth=12.0).build()
    assert isinstance(result, OpenSCADObject)


def test_render_writes_scad(tmp_path: Path) -> None:
    """render() produces a .scad file in the output directory."""
    part = GeneralPipeClamp()
    part.render(tmp_path)
    scad_files = list(tmp_path.glob("*.scad"))
    assert scad_files, f"No .scad files found in {tmp_path}"
