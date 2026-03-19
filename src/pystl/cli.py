"""Shared CLI helpers for pystl scripts."""

import argparse
import dataclasses
import logging
from pathlib import Path
from typing import Any

from pystl.py_stl_base import PyStlPart


def setup_logging() -> None:
    """Configure root logger at INFO level with a simple format."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")


def add_part_args(parser: argparse.ArgumentParser, part_cls: type[PyStlPart]) -> None:
    """Add dataclass fields of part_cls as typed --field_name arguments.

    Args:
        parser: The argument parser to add arguments to.
        part_cls: The part dataclass whose fields become CLI arguments.
    """
    for field in dataclasses.fields(part_cls):
        field_type = (
            field.type if isinstance(field.type, type) else eval(field.type)  # noqa: S307
        )
        parser.add_argument(
            f"--{field.name}",
            type=field_type,
            default=None,
            metavar=str(field.default),
            help=f"{field.name} (default: {field.default})",
        )


def build_part(part_cls: type[PyStlPart], args: argparse.Namespace) -> PyStlPart:
    """Instantiate part_cls using only its dataclass fields from args.

    Args:
        part_cls: The part class to instantiate.
        args: Parsed argument namespace; non-None field values are passed as kwargs.

    Returns:
        An instance of part_cls with the specified parameters.
    """
    field_names = {f.name for f in dataclasses.fields(part_cls)}
    kwargs: dict[str, Any] = {
        k: v for k, v in vars(args).items() if k in field_names and v is not None
    }
    return part_cls(**kwargs)


def build_and_render(part_cls: type[PyStlPart], description: str | None = None) -> None:
    """Parse CLI arguments and render part_cls to .scad/.stl.

    Encapsulates the standard main() pattern for part scripts:
    sets up logging, builds an ArgumentParser with --outdir and all
    dataclass fields as flags, then renders with the parsed values.

    Args:
        part_cls: The part class to instantiate and render.
        description: Argparse description string. Defaults to
            "Render <ClassName> to .scad / .stl".
    """
    setup_logging()
    desc = description or f"Render {part_cls.__name__} to .scad / .stl"
    parser = argparse.ArgumentParser(description=desc)
    add_output_arg(parser)
    add_part_args(parser, part_cls)
    args = parser.parse_args()
    build_part(part_cls, args).render(Path(args.outdir))


def add_output_arg(parser: argparse.ArgumentParser, default: str = "output") -> None:
    """Add --outdir argument to parser.

    Args:
        parser: The argument parser to add the argument to.
        default: Default output directory path.
    """
    parser.add_argument(
        "--outdir",
        default=default,
        help=f"Output directory (default: {default})",
    )
