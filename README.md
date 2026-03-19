# pystl

PYthon STL generation using [SolidPython2](https://github.com/jeff-dh/SolidPython).

Library parts are defined as Python dataclasses with a `build()` method that
returns an `OpenSCADObject`. Library parts can be composed together or combined
with custom code before being emitted as a `.scad` and/or `.stl` file.

The library comes with a few pre-defined parts.  If you find yourself repeatedly
using custom code, you can create a new Python dataclass for future use.

The usual workflow is to:
* copy `scripts/boilerplate.py` to `scripts/my_custom_part.py`
* Edit `scripts/my_custom_part.py`, implementing `build()` and adding
argparse parameters for your part as needed
* run `uv run python scripts/my_custom_part.py` with appropriate command line 
arguments to generate .scad and .stl files

## One-time setup

Requires Python ≥ 3.10 and [uv](https://docs.astral.sh/uv/).

```bash
git clone <repo>
cd pystl
uv sync           # initilize the required packagers
```

STL export requires the [OpenSCAD](https://openscad.org/downloads.html) CLI to 
be in `PATH`.  

## Render parts

```bash
# Render with defaults
uv run python scripts/example_bracket.py

# Render with parameter overrides
uv run python scripts/example_bracket.py --height=20 --width=25

# Write output to a custom directory
uv run python scripts/example_bracket.py --outdir /tmp/prints

# See all available parameters
uv run python scripts/example_bracket.py --help
```

By default, output files land in `output/` (gitignored):

```
output/
  ExampleBracket.scad   ← OpenSCAD source, inspect or tweak in the OpenSCAD GUI
  ExampleBracket.stl    ← ready to slice (requires openscad in PATH)
```

## Adding a new part

1. Copy the boilerplate:

   ```bash
   cp scripts/boilerplate.py scripts/my_custom_part.py
   ```

2. Edit `scripts/my_custom_part.py`:
   - Rename `MyCustomPart` to your class name (update the argparse description too)
   - Add `@dataclass` fields for your parameters (each becomes a CLI flag automatically)
   - Implement `build()` — compose library parts from `src/pystl/library/` and/or raw
     SolidPython2 primitives into your final assembly
   - Add extra argparse flags in `main()` if needed beyond the auto-generated ones

3. Render and verify:

   ```bash
   uv run python scripts/my_custom_part.py
   uv run python scripts/my_custom_part.py --help   # inspect available flags
   ```

> **Tip:** A `scripts/new_part.py` generator is planned that will scaffold the boilerplate
> automatically: `uv run python scripts/new_part.py MyCustomPart`

## Viewing parts

Install [OpenSCAD](https://openscad.org/downloads.html) to inspect or tweak the `.scad` source interactively, and to enable STL export.

**macOS**
```bash
open output/ExampleBracket.scad          # opens in OpenSCAD if associated
# or, explicitly:
/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD output/ExampleBracket.scad
```

**Linux**
```bash
openscad output/ExampleBracket.scad
```

**Windows** (PowerShell)
```powershell
& "C:\Program Files\OpenSCAD\openscad.exe" output\ExampleBracket.scad
```

The `.stl` files can be viewed in any .stl viewer and opened directly in any 
slicer (PrusaSlicer, Bambu Studio, Cura, etc.).

## SolidPython2 API reference

- **GitHub / docs:** https://github.com/jeff-dh/SolidPython
- **Primitives:** `cube`, `sphere`, `cylinder`, `polyhedron`, …
- **Transforms:** `.translate()`, `.rotate()`, `.scale()`, `.mirror()`, …
- **Boolean ops:** `a + b` (union), `a - b` (difference), `a * b` (intersection)
- **Output:** `model.save_as_scad("file.scad")` · STL via `openscad -o file.stl file.scad`

## Development

```bash
uv run pytest                        # tests
uv run ruff check . && uv run ruff format .   # lint + format
uv run mypy src/                     # type check
```

## Project structure

```
src/pystl/
  py_stl_base.py   — PyStlPart base class (build + render)
  cli.py           — shared argparse/logging helpers used by all scripts
  library/         — reusable sub-parts
    __init__.py
    general_pipe_clamp.py
    filleted_rect.py
    …
scripts/
  boilerplate.py           — template: copy this to create a new part script
  example_bracket.py       — example custom part
  new_part.py              — (planned) scaffold a new part script from boilerplate
  …
tests/             — pytest suite
output/            — generated .scad and .stl (gitignored)
```
