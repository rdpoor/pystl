# hex_socket_caps.py
import math
from typing import Dict, Optional, Tuple
from dataclasses import dataclass

@dataclass(frozen=True)
class HexSocketCap:
    name: str
    thread_pitch: float
    head_diameter_max: float
    head_height_max: float
    key_size: float

    @property
    def head_diameter(self) -> float:
        """Return the max diameter"""
        return self.head_diameter_max

    @property
    def head_radius(self) -> float:
        """Return the max head radius."""
        return self.head_diameter_max / 2

    @property
    def head_height(self) -> float:
        """Return the nominal head depth (average of min and max)."""
        return self.head_height_max

# Load immediately at module import
_HEX_SOCKET_CAPS: Dict[str, HexSocketCap] = {
    # Nominal Size    Thread Pitch    Head Dia (Max)  Head Height (Max)   Key Size (Allen)
    'M3': HexSocketCap('M3',  0.5,  5.5,  3.0,  2.5),
    'M4': HexSocketCap('M4', 0.7,  7.0,  4.0,  3.0),
    'M5': HexSocketCap('M5', 0.8,  8.5,  5.0,  4.0),
    'M6': HexSocketCap('M6', 1.0,  10.0, 6.0,  5.0),
    'M8': HexSocketCap('M8', 1.25, 13.0, 8.0,  6.0),
    'M10': HexSocketCap('M10', 1.5,  16.0, 10.0, 8.0),
    'M12': HexSocketCap('M12', 1.75, 18.0, 12.0, 10.0),
    'M16': HexSocketCap('M16', 2.0,  24.0, 16.0, 14.0),
    'M20': HexSocketCap('M20', 2.5,  30.0, 20.0, 17.0),
}

def get(name: str) -> Optional[HexNut]:
    """Get a socket cap by name."""
    return _HEX_SOCKET_CAPS.get(name)

def names() -> Tuple[str, ...]:
    """Return all available names."""
    return tuple(_HEX_SOCKET_CAPS.keys())

# Usage
# import hex_socket_caps
# m12 = hex_socket_caps.get('M12')
# print(m12.head_diameter)  # 18.0
