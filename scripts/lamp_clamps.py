# Create 4 pipem clamps to hold lamp assembly:
# uv run python scripts/lamp_clamps.py --level upper --side left
# uv run python scripts/lamp_clamps.py --level lower --side left
# uv run python scripts/lamp_clamps.py --level upper --side right
# uv run python scripts/lamp_clamps.py --level lower --side right

import argparse

import pystl.library.hex_nuts as hex_nuts
from pystl.library.pipe_clamp import PipeClamp
from pystl.library.py_stl_inset import HexNutInset
from pystl.py_stl_geometry import PyStlGeometry
from pystl.py_stl_part import PyStlPart
from pystl.utils import setup_logging, write_model

YELNATS_FORK_DIAMETER = 45
YELNATS_FORK_RADIUS = YELNATS_FORK_DIAMETER / 2
CLAMP_HEIGHT = 20
CLAMP_THICKNESS = 5

FRONT_TAB_GAP = 3
FRONT_TAB_THICKNESS = FRONT_TAB_GAP + CLAMP_THICKNESS * 1.5
LEFT_FRONT_TAB_OFFSET = 3
RIGHT_FRONT_TAB_OFFSET = -3

REAR_TAB_GAP = 1
REAR_TAB_THICKNESS = REAR_TAB_GAP + CLAMP_THICKNESS * 1.5
UPPER_TAB_LENGTH = YELNATS_FORK_RADIUS + 32
LOWER_TAB_LENGTH = YELNATS_FORK_RADIUS + 28
REAR_TAB_LENGTH = YELNATS_FORK_RADIUS + 10
TURN_SIGNAL_BOLT_DIAMETER = 10.1
M4_DRILL_DIAMETER = 4.3

def make_clamp(level, side) -> PyStlGeometry:
    m4_inset = HexNutInset(depth=2, nut=hex_nuts.get('M4'))
    model = (PipeClamp(
        inner_diameter=YELNATS_FORK_DIAMETER,
        wall_thickness=CLAMP_THICKNESS,
        height=CLAMP_HEIGHT,
        fn=128)
    ).add_tab(  # rear tab
        width=REAR_TAB_THICKNESS,
        length=REAR_TAB_LENGTH,
        angle=0,
        offset=0,
        drill_diameter=M4_DRILL_DIAMETER,
        split_gap_width=REAR_TAB_GAP,
        front_inset=m4_inset if side=='right' else None,
        rear_inset=m4_inset if side=='left' else None,
        fn=128,
    ).add_tab(  # front tab
        width=FRONT_TAB_THICKNESS,
        length=UPPER_TAB_LENGTH if level=='upper' else LOWER_TAB_LENGTH,
        angle=180,
        offset=LEFT_FRONT_TAB_OFFSET if side=='left' else RIGHT_FRONT_TAB_OFFSET,
        drill_diameter=TURN_SIGNAL_BOLT_DIAMETER if level=='upper' else M4_DRILL_DIAMETER,
        split_gap_width=FRONT_TAB_GAP,
        front_inset=m4_inset if side=='left' and level=='lower' else None,
        rear_inset=m4_inset if side=='right' and level=='lower'else None,
        fn=128,
    )
    return model

def main() -> None:
    """render offset lamp clamp."""
    setup_logging()
    parser = argparse.ArgumentParser(
        description="Render clamps to hold headlight to front fork."
    )
    parser.add_argument(
        "--side",
        required=True,
        choices=["left", "right"],
        help="which fork tube the clamp goes on",
    )
    parser.add_argument(
        "--level",
        required=True,
        choices=["upper", "lower"],
        help="upper or lower clamp",
    )
    args = parser.parse_args()
    model = make_clamp(args.level, args.side)
    write_model(model.build().combined(), f"output/{args.level}_{args.side}_lamp_clamp")

if __name__ == "__main__":
    main()
