# test_pipe_clamp.py

from pystl.library import hex_nuts
from pystl.library.pipe_clamp import PipeClamp
from pystl.library.py_stl_inset import (
    CircularInset,
    HexNutInset,
    CountersinkInset,
    SlottedArcInset)
from pystl.utils import setup_logging, write_model

setup_logging()

WALL_THICKNESS = 10
HEADSTOCK_DIAMETER = 33
CLAMP_HEIGHT = 14
CLAMP_THICKNESS = 10
FRONT_TAB_LENGTH = 64
LAMP_CLAMP_SPLIT = 37.5
LAMP_CLAMP_TAB_WIDTH = 7

inset_a = HexNutInset(depth=2, nut=hex_nuts.get('M4'))
model = (PipeClamp(
    inner_diameter=HEADSTOCK_DIAMETER,
    wall_thickness=WALL_THICKNESS,
    height=CLAMP_THICKNESS,
    )
    .add_tab(
        angle=0,
        width=WALL_THICKNESS,
        length=HEADSTOCK_DIAMETER/2 + 15,
        drill_diameter=4.1,
        split_gap_width=3,
        front_inset=inset_a)
    .add_tab(
        angle=180,
        width=10,
        length=HEADSTOCK_DIAMETER/2 + WALL_THICKNESS/2,
        drill_diameter=4.1,
        split_gap_width=3,
        front_inset=inset_a)
    .add_tab(
        angle=180,
        width=LAMP_CLAMP_TAB_WIDTH,
        length=FRONT_TAB_LENGTH,
        offset=LAMP_CLAMP_SPLIT/2 + LAMP_CLAMP_TAB_WIDTH/2,
        drill_diameter=5,
        split_gap_width=0)
    .add_tab(
        angle=180,
        width=LAMP_CLAMP_TAB_WIDTH,
        length=FRONT_TAB_LENGTH,
        offset=-LAMP_CLAMP_SPLIT/2 - LAMP_CLAMP_TAB_WIDTH/2,
        drill_diameter=5,
        split_gap_width=0))
write_model(model.build().combined(), "output/grit_shift_clamp")
