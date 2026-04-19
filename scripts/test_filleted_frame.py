# test_pipe_clamp.py

from pystl.library import hex_nuts
from pystl.library.filleted_rect import FilletedFrame
from pystl.utils import setup_logging, write_model

setup_logging()

model = FilletedFrame(
    outer_width=50,
    outer_height=30,
    frame_thickness=10,
    outer_radius=20
    )
write_model(model.build().combined(), "output/test_frame")
