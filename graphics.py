"""
OpenGL rendering helpers: texture loading and cube drawing.
"""

import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from config import textures


def load_texture(path: str) -> int:
    """Load a texture from an image file and bind it to OpenGL."""
    surface = pygame.image.load(path)
    texture_data = pygame.image.tostring(surface, "RGB", True)
    width, height = surface.get_size()

    glEnable(GL_TEXTURE_2D)
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0,
                 GL_RGB, GL_UNSIGNED_BYTE, texture_data)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    return texture_id


def draw_textured_cuboid(size, texture_id: str) -> None:
    """Draw a textured cuboid at the origin with given size."""
    width, height, depth = size

    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, textures[texture_id])
    # print("draw", textures[texture_id])
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
    glColor3f(1, 1, 1)

    glBegin(GL_QUADS)

    def v(p): return (p[0] * width, p[1] * height, p[2] * depth)

    faces = [
        [v((0,0,0)), v((1,0,0)), v((1,1,0)), v((0,1,0))],  # Back
        [v((0,0,1)), v((1,0,1)), v((1,1,1)), v((0,1,1))],  # Front
        [v((0,0,0)), v((1,0,0)), v((1,0,1)), v((0,0,1))],  # Bottom
        [v((0,1,0)), v((1,1,0)), v((1,1,1)), v((0,1,1))],  # Top
        [v((1,0,0)), v((1,1,0)), v((1,1,1)), v((1,0,1))],  # Right
        [v((0,0,0)), v((0,1,0)), v((0,1,1)), v((0,0,1))],  # Left
    ]

    tex = [(0,0), (1,0), (1,1), (0,1)]
    for face in faces:
        for i in range(4):
            glTexCoord2fv(tex[i])
            glVertex3fv(face[i])
    glEnd()

    glDisable(GL_TEXTURE_2D)
