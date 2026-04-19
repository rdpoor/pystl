# hex_nuts.py
import math
from typing import Dict, Optional, Tuple
from dataclasses import dataclass


@dataclass(frozen=True)
class HexNut:
    name: str
    thread_pitch: float
    width_across_flats: float
    width_across_corners: float
    thickness_min: float
    thickness_max: float

    @property
    def inset_diameter(self) -> float:
        """Return the circumscribed circle diameter (vertex-to-vertex distance)."""
        return self.width_across_flats * 2 / math.sqrt(3)

    @property
    def inset_radius(self) -> float:
        """Return the circumscribed circle radius (center to vertex)."""
        return self.width_across_flats / math.sqrt(3)

    @property
    def thickness_nom(self) -> float:
        """Return the nominal thickness (average of min and max)."""
        return (self.thickness_min + self.thickness_max) / 2


# Load immediately at module import
_NUTS: Dict[str, HexNut] = {
    "M1.6": HexNut("M1.6", 0.35, 3.2, 3.41, 1.05, 1.30),
    "M2": HexNut("M2", 0.4, 4.0, 4.32, 1.35, 1.60),
    "M2.5": HexNut("M2.5", 0.45, 5.0, 5.45, 1.75, 2.00),
    "M3": HexNut("M3", 0.5, 5.5, 6.01, 2.15, 2.40),
    "M4": HexNut("M4", 0.7, 7.0, 7.66, 2.90, 3.20),
    "M5": HexNut("M5", 0.8, 8.0, 8.79, 4.40, 4.70),
    "M6": HexNut("M6", 1.0, 10.0, 11.05, 4.90, 5.20),
    "M8": HexNut("M8", 1.25, 13.0, 14.38, 6.44, 6.80),
    "M10": HexNut("M10", 1.5, 16.0, 17.77, 8.04, 9.10),
    "M12": HexNut("M12", 1.75, 18.0, 20.03, 10.37, 10.80),
    "M14": HexNut("M14", 2.0, 21.0, 23.35, 12.10, 12.80),
    "M16": HexNut("M16", 2.0, 24.0, 26.75, 14.10, 14.80),
    "M20": HexNut("M20", 2.5, 30.0, 32.95, 16.90, 18.00),
    "M24": HexNut("M24", 3.0, 36.0, 39.55, 20.20, 21.50),
    "M30": HexNut("M30", 3.5, 46.0, 50.85, 24.30, 25.60),
    "M36": HexNut("M36", 4.0, 55.0, 60.79, 29.40, 31.00),
}


def get(name: str) -> Optional[HexNut]:
    """Get a nut by name."""
    return _NUTS.get(name)


def names() -> Tuple[str, ...]:
    """Return all available names."""
    return tuple(_NUTS.keys())


# Usage
# import hex_nuts
# m12 = hex_nuts.get('M12')
# print(m12.thickness_nom)  # 10.585
