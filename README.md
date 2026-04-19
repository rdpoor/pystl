# pystl

PYthon STL generation using [SolidPython2](https://github.com/jeff-dh/SolidPython).

Library parts are defined as Python dataclasses with a `build()` method that
returns an `OpenSCADObject`. Library parts can be composed together or combined
with custom code before being emitted as a `.scad` and/or `.stl` file.

The usual workflow is to add a script under `scripts/` that subclasses
`PyStlPart` (see `scripts/lamp_side_panel.py`) or calls `write_model()` for
ad-hoc geometry (see `scripts/lamp_clamp.py`), then run it with `uv run`.

## One-time setup

Requires Python ≥ 3.10 and [uv](https://docs.astral.sh/uv/).

```bash
git clone <repo>
cd pystl
uv sync
```

STL export requires the [OpenSCAD](https://openscad.org/downloads.html) CLI to
be in `PATH`.

## Render parts

```bash
# PyStlPart-based script (defaults + help)
uv run python scripts/lamp_side_panel.py
uv run python scripts/lamp_side_panel.py --help

# Custom output directory
uv run python scripts/lamp_side_panel.py --outdir /tmp/prints
```

By default, output files land in `output/` (gitignored). Exact filenames depend
on the part class or script.

## Viewing parts

Install [OpenSCAD](https://openscad.org/downloads.html) to inspect or tweak the
`.scad` source interactively, and to enable STL export.

**Windows** (PowerShell)

```powershell
& "C:\Program Files\OpenSCAD\openscad.exe" output\<YourPart>.scad
```

**macOS**

```bash
open output/<YourPart>.scad
```

**Linux**

```bash
openscad output/<YourPart>.scad
```

## SolidPython2 API reference

- **GitHub / docs:** https://github.com/jeff-dh/SolidPython
- **Primitives:** `cube`, `sphere`, `cylinder`, `polyhedron`, …
- **Transforms:** `.translate()`, `.rotate()`, `.scale()`, `.mirror()`, …
- **Boolean ops:** `a + b` (union), `a - b` (difference), `a * b` (intersection)
- **Output:** `model.save_as_scad("file.scad")` · STL via `openscad -o file.stl file.scad`

## Development

```bash
uv run pytest
uv run ruff check . && uv run ruff format .
uv run mypy src/
```

## Project structure

```
src/pystl/
  py_stl_base.py   — PyStlPart base class (build + render)
  cli.py           — shared argparse/logging helpers used by scripts
  utils.py         — write_model, logging setup
  library/         — reusable sub-parts
scripts/           — one script per printable assembly / experiment
tests/             — pytest suite
output/            — generated .scad and .stl (gitignored)
```

See `CLAUDE.md` for conventions and tooling details.
