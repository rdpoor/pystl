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

inset_a = HexNutInset(depth=2, nut=hex_nuts.get('M4'))
inset_b = CountersinkInset(depth=5, diameter=6)
inset_c = SlottedArcInset(depth=5, start_deg=-20, end_deg=20, radius=3, slot_width=1.2)
model = (PipeClamp()
    .add_tab(angle=90, length=40, front_inset=inset_a)
    .add_tab(angle=180, offset=4, rear_inset=inset_b)
    .add_tab(angle=275, length=50, front_inset=inset_c))
write_model(model.build().combined(), "output/pipe_clamp")
