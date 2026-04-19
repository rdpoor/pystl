"""Base class for parametric parts."""

from dataclasses import dataclass
from typing import ClassVar

from pystl.py_stl_geometry import PyStlGeometry


@dataclass
class PyStlPart:
    """Base class for pystl parts. Subclass and implement :meth:`build`."""

    CUT_CLEARANCE: ClassVar[float] = 0.01

    def build(self) -> PyStlGeometry:
        """Return positive and negative geometry for this part.

        Raises:
            NotImplementedError: Subclasses must implement this method.
        """
        raise NotImplementedError
