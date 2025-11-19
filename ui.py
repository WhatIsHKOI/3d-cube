"""
2D UI rendering using pygame surfaces.
"""

import pygame
from typing import Tuple
from config import FONT_PATH


def draw_text(surface: pygame.Surface, text: str, box: Tuple[int, int, int, int],
              size: int = 32, color=(255, 255, 255), align: str = "center") -> None:
    """
    Render text inside a rectangular box on a pygame surface.

    Parameters:
        surface (pygame.Surface): Destination surface to draw on.
        text (str): Text string to render.
        box (Tuple[int, int, int, int]): (x1, y1, x2, y2) rectangle coordinates.
        size (int): Font size.
        color (Tuple[int, int, int]): RGB color.
        align (str): Horizontal alignment ('left', 'center', 'right').
    """
    font = pygame.font.Font(FONT_PATH, size)
    text_surface = font.render(text, True, color)
    w, _ = text_surface.get_size()

    x1, y1, x2, _ = box
    box_w = x2 - x1

    if align == "left":
        x = x1
    elif align == "center":
        x = x1 + (box_w - w) // 2
    elif align == "right":
        x = x2 - w
    else:
        x = x1

    surface.blit(text_surface, (x, y1))
