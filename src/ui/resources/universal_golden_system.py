import math
from dataclasses import dataclass
from typing import Dict


@dataclass
class Dimensions:
    width: int
    height: int


class UniversalGoldenSystem:
    """Système universel du nombre d'or pour toute l'interface."""

    # Constantes mathématiques (φ)
    PHI: float = (1 + math.sqrt(5)) / 2  # 1.618033988749895
    PHI_INV: float = 1 / PHI             # 0.618033988749895
    PHI_SQUARED: float = PHI * PHI       # 2.618033988749895

    # Dimensions base
    BASE_WINDOW_WIDTH: int = 1400
    BASE_WINDOW_HEIGHT: int = 900

    @classmethod
    def get_main_layout_dimensions(cls, window_width: int | None = None) -> Dict[str, int]:
        """Dimensions principales selon φ pour une largeur donnée."""
        width = window_width or cls.BASE_WINDOW_WIDTH
        sidebar_width = int(width * (1 - cls.PHI_INV))  # 38.2%
        content_width = width - sidebar_width           # 61.8%
        main_column_width = int(content_width * cls.PHI_INV)
        side_column_width = content_width - main_column_width
        return {
            "window_width": width,
            "sidebar_width": sidebar_width,
            "content_width": content_width,
            "main_column_width": main_column_width,
            "side_column_width": side_column_width,
        }

    @classmethod
    def get_height_sequence(cls, base_height: int = 300) -> Dict[str, int]:
        """Séquence de hauteurs basée sur φ (px)."""
        return {
            "header": int(base_height / (cls.PHI ** 3)),  # ~68px
            "section_xl": base_height,                    # 300px
            "section_l": int(base_height / cls.PHI),      # ~185px
            "section_m": int(base_height / cls.PHI_SQUARED),  # ~114px
            "section_s": int(base_height / (cls.PHI ** 3)),   # ~68px
            "button": int(base_height / (cls.PHI ** 2.5)),    # ~45px
            "label": int(base_height / (cls.PHI ** 3.5)),     # ~28px
        }

    @classmethod
    def get_spacing_system(cls, base_unit: int = 8) -> Dict[str, int]:
        return {
            "xs": base_unit,                   # 8
            "sm": int(base_unit * cls.PHI**0.5),
            "md": int(base_unit * cls.PHI),
            "lg": int(base_unit * cls.PHI_SQUARED),
            "xl": int(base_unit * (cls.PHI ** 2.5)),
        }

    @classmethod
    def get_font_sizes(cls, base_font: int = 14) -> Dict[str, int]:
        return {
            "tiny": int(base_font / cls.PHI_SQUARED),
            "small": int(base_font / cls.PHI),
            "base": base_font,
            "medium": int(base_font * cls.PHI ** 0.5),
            "large": int(base_font * cls.PHI),
            "xl": int(base_font * cls.PHI_SQUARED),
            "xxl": int(base_font * (cls.PHI ** 2.5)),
        }

    @classmethod
    def validate_proportions(cls, main_width: int, total_width: int) -> bool:
        ratio = main_width / total_width
        return abs(ratio - cls.PHI_INV) < 0.01

    @classmethod
    def calculate_responsive_layout(cls, available_width: int, available_height: int) -> Dict[str, Dict[str, int]]:
        dims = cls.get_main_layout_dimensions(available_width)
        heights = cls.get_height_sequence(int(available_height * 0.3) or 300)
        spacing = cls.get_spacing_system()
        fonts = cls.get_font_sizes()
        return {
            "dimensions": dims,
            "heights": heights,
            "spacing": spacing,
            "fonts": fonts,
            "is_valid": cls.validate_proportions(dims["main_column_width"], dims["content_width"]),
        }


