#!/usr/bin/env python3
"""Smoke-test a library part: instantiate with defaults and render to .scad/.stl.

Usage:
    uv run python scripts/test_library_part.py --part GeneralPipeClamp
    uv run python scripts/test_library_part.py --part FilletedRect --outdir /tmp/out
"""

import argparse
import importlib
import pkgutil
import sys
from pathlib import Path

import pystl.library
from pystl.cli import setup_logging
from pystl.py_stl_base import PyStlPart


def _find_part_class(name: str) -> type[PyStlPart] | None:
    """Search all pystl.library submodules for a PyStlPart subclass named *name*.

    Args:
        name: The class name to look for.

    Returns:
        The matching class, or None if not found.
    """
    for _importer, modname, _ispkg in pkgutil.iter_modules(pystl.library.__path__):
        module = importlib.import_module(f"pystl.library.{modname}")
        cls = getattr(module, name, None)
        if isinstance(cls, type) and issubclass(cls, PyStlPart):
            return cls
    return None


def main() -> None:
    """Parse --part <ClassName>, instantiate with defaults, and render."""
    setup_logging()
    parser = argparse.ArgumentParser(
        description="Render a library part with default parameters."
    )
    parser.add_argument(
        "--part",
        required=True,
        help="Class name of the library part to render (e.g. GeneralPipeClamp)",
    )
    parser.add_argument(
        "--outdir",
        default="output",
        help="Output directory (default: output)",
    )
    args = parser.parse_args()

    part_cls = _find_part_class(args.part)
    if part_cls is None:
        print(f"Error: '{args.part}' not found in pystl.library", file=sys.stderr)
        sys.exit(1)

    part_cls().render(Path(args.outdir))


if __name__ == "__main__":
    main()
