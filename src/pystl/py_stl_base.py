"""Base class and render utilities for pystl parts."""

import logging
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

from solid2.core.object_base import OpenSCADObject

log = logging.getLogger(__name__)


@dataclass
class PyStlPart:
    """Base class for all pystl parts. Subclass and implement build()."""

    def build(self) -> OpenSCADObject:
        """Build and return the OpenSCAD model for this part.

        Returns:
            The SolidPython2 model object.

        Raises:
            NotImplementedError: Subclasses must implement this method.
        """
        raise NotImplementedError

    def render(self, output_dir: Path) -> None:
        """Render this part to .scad and optionally .stl in output_dir.

        Args:
            output_dir: Directory where output files will be written.
        """
        output_dir.mkdir(parents=True, exist_ok=True)
        name = type(self).__name__
        model = self.build()

        scad_path = output_dir / f"{name}.scad"
        model.save_as_scad(str(scad_path))
        log.info("Wrote %s", scad_path)

        stl_path = output_dir / f"{name}.stl"
        if shutil.which("openscad") is not None:
            subprocess.run(
                ["openscad", "-o", str(stl_path), str(scad_path)],
                check=True,
            )
            log.info("Wrote %s", stl_path)
        else:
            log.warning("openscad not found in PATH; skipping STL export for %s", name)
