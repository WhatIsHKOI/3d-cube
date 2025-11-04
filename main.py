import math
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *


#Initialization
pygame.init()
display = (800, 600)
pygame.display.set_mode(display, DOUBLEBUF|OPENGL)


# Load texture
def load_texture(path):
    texture_surface = pygame.image.load(path)
    texture_data = pygame.image.tostring(texture_surface, "RGB", True)
    width, height = texture_surface.get_size()

    glEnable(GL_TEXTURE_2D)
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, texture_data)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    return texture_id

texture_id = load_texture("assets/cube_texture.png")


# OpenGL setup
glEnable(GL_DEPTH_TEST)
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
glMatrixMode(GL_MODELVIEW)
zoom = -5.0
glTranslatef(0.0, 0.0, zoom)


def draw_textured_cube_at(x, y, z):
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glBegin(GL_QUADS)

    # Offset all vertices by (x, y, z)
    def V(v): return (v[0] + x, v[1] + y, v[2] + z)

    # Define cube faces using offset vertices
    face_vertices = [
        # Back face
        (V((0, 0, 0)), V((2, 0, 0)), V((2, 2, 0)), V((0, 2, 0))),
        # Front face
        (V((0, 0, 2)), V((2, 0, 2)), V((2, 2, 2)), V((0, 2, 2))),
        # Bottom face
        (V((0, 0, 0)), V((2, 0, 0)), V((2, 0, 2)), V((0, 0, 2))),
        # Top face
        (V((0, 2, 0)), V((2, 2, 0)), V((2, 2, 2)), V((0, 2, 2))),
        # Right face
        (V((2, 0, 0)), V((2, 2, 0)), V((2, 2, 2)), V((2, 0, 2))),
        # Left face
        (V((0, 0, 0)), V((0, 2, 0)), V((0, 2, 2)), V((0, 0, 2))),
    ]

    tex_coords = [(0, 0), (1, 0), (1, 1), (0, 1)]

    for face in face_vertices:
        for i in range(4):
            glTexCoord2fv(tex_coords[i])
            glVertex3fv(face[i])
    glEnd()

# Main game
running = 1
dragging = False
last_mouse_pos = None
sx_angle = 0
sy_angle = 0
sz_angle = 0
camera_y = 0
cube_pos = [-1.0, -1.0, -1.0]

while running:

    # Each frame initialize variables
    x_angle = 0
    y_angle = 0
    z_angle = 0

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                dragging = True
                last_mouse_pos = pygame.mouse.get_pos()

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                dragging = False
            elif event.button == 4:  # Scroll up
                zoom += 0.5  # Zoom in
            elif event.button == 5:  # Scroll down
                zoom -= 0.5  # Zoom out

        elif event.type == pygame.MOUSEMOTION and dragging:
            y, x = pygame.mouse.get_pos()
            dx = x - last_mouse_pos[1]
            dy = y - last_mouse_pos[0]

            # Horizontal drag → X-axis rotation
            y_angle += dy * 0.5

            # Vertical drag → Y and Z-axis rotation
            x_angle += dx * 0.5

            last_mouse_pos = (y, x)

    keys = pygame.key.get_pressed()
    if keys[K_ESCAPE]:
        pygame.quit()
        quit()

    if keys[K_LEFT]:
        cube_pos[0] -= 0.1
    if keys[K_RIGHT]:
        cube_pos[0] += 0.1
    if keys[K_UP]:
        cube_pos[2] -= 0.1
    if keys[K_DOWN]:
        cube_pos[2] += 0.1
    if keys[K_w]:
        camera_y += 0.1  # Move camera up
    if keys[K_s]:
        camera_y -= 0.1  # Move camera down
    
    sx_angle = (sx_angle + x_angle + 360) % 360
    sy_angle = (sy_angle + y_angle + 360) % 360
    sz_angle = (sz_angle + z_angle + 360) % 360

    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0.0, -camera_y, zoom)
    glRotatef(sx_angle, 1, 0, 0)
    glRotatef(sy_angle, 0, 1, 0)
    glRotatef(sz_angle, 0, 0, 1)
    draw_textured_cube_at(cube_pos[0], cube_pos[1], cube_pos[2])
    pygame.display.flip()
    pygame.time.wait(10)
