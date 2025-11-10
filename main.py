import math
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import time

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

def intersect_rect(r1, r2):
    # r1 and r2 are tuples: (x, y, side_length)
    x1, y1, s1 = r1
    x2, y2, s2 = r2

    # Compute overlap boundaries
    left = max(x1, x2)
    right = min(x1 + s1, x2 + s2)
    bottom = max(y1, y2)
    top = min(y1 + s1, y2 + s2)

    # Check for intersection
    if left < right and bottom < top:
        return (left, bottom, right - left, top - bottom)  # (x, y, width, height)
    else:
        return None  # No intersection

def draw_textured_cuboid_at(x, y, z, width, height, depth):
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glBegin(GL_QUADS)

    # Offset and scale vertices
    def V(v): return (v[0] * width + x, v[1] * height + y, v[2] * depth + z)

    # Define cuboid faces
    face_vertices = [
        # Back face
        (V((0, 0, 0)), V((1, 0, 0)), V((1, 1, 0)), V((0, 1, 0))),
        # Front face
        (V((0, 0, 1)), V((1, 0, 1)), V((1, 1, 1)), V((0, 1, 1))),
        # Bottom face
        (V((0, 0, 0)), V((1, 0, 0)), V((1, 0, 1)), V((0, 0, 1))),
        # Top face
        (V((0, 1, 0)), V((1, 1, 0)), V((1, 1, 1)), V((0, 1, 1))),
        # Right face
        (V((1, 0, 0)), V((1, 1, 0)), V((1, 1, 1)), V((1, 0, 1))),
        # Left face
        (V((0, 0, 0)), V((0, 1, 0)), V((0, 1, 1)), V((0, 0, 1))),
    ]

    tex_coords = [(0, 0), (1, 0), (1, 1), (0, 1)]

    for face in face_vertices:
        for i in range(4):
            glTexCoord2fv(tex_coords[i])
            glVertex3fv(face[i])
    glEnd()

def game():

    # Main game
    running = 1
    dragging = False
    last_mouse_pos = None
    last_spawn_time = time.time()
    force_quit_interval = 10
    cube_y = 0
    azimuth = 0.0      # Horizontal angle (left/right)
    elevation = 30.0   # Vertical angle (up/down)
    radius = 10.0      # Distance from target (zoom)
    target = [0.0, 0.0, 0.0]  # Point to orbit around
    frame_counter = 0 # Debug use
    space_pressed = False # Check spacebar pressed

    # Cube data structure
    cubes = [{
        "pos": [-1.0, -1.0, -1.0],
        "rot": [0.0, 0.0, 0.0]
    }]

    while running:

        # Each frame initialize variables
        x_angle = 0
        y_angle = 0
        z_angle = 0
        current_time = time.time()

        if current_time - last_spawn_time >= force_quit_interval:
            lose()

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
                    radius -= 0.5  # Zoom in
                elif event.button == 5:  # Scroll down
                    radius += 0.5  # Zoom out

            elif event.type == pygame.MOUSEMOTION and dragging:
                x, y = pygame.mouse.get_pos()
                dx = x - last_mouse_pos[0]
                dy = y - last_mouse_pos[1]
                
                azimuth -= dx * 0.3
                elevation += dy * 0.3
                elevation = max(-89.9, min(89.9, elevation))  # Clamp to avoid gimbal lock

                last_mouse_pos = (x, y)
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    space_pressed = False

        keys = pygame.key.get_pressed()
        if keys[K_ESCAPE]:
            pygame.quit()
            quit()

        if keys[K_w]:
            cube_y += 0.1  # Move camera up
        if keys[K_s]:
            cube_y -= 0.1  # Move camera down
        if keys[K_SPACE]:
            if space_pressed == False:
                new_cube = {
                    "pos": [cubes[-1]["pos"][0]+3, cubes[-1]["pos"][1]+1.0, cubes[-1]["pos"][2]],
                    "rot": [cubes[-1]["rot"][0], cubes[-1]["rot"][1], cubes[-1]["rot"][2]]
                }
                cubes.append(new_cube)
                last_spawn_time = current_time

                print("new cube, cube stack size =", len(cubes))
                print("frame =", frame_counter)
            space_pressed = True
        
        elif len(cubes) != 1:
            cubes[-1]["pos"][0] -= 0.01
        
        cubes[-1]["rot"][0] = (cubes[-1]["rot"][0] + x_angle + 360) % 360
        cubes[-1]["rot"][1] = (cubes[-1]["rot"][1] + y_angle + 360) % 360
        cubes[-1]["rot"][2] = (cubes[-1]["rot"][2] + z_angle + 360) % 360

        cam_x = 0 + radius * math.cos(math.radians(elevation)) * math.sin(math.radians(azimuth))
        cam_y = cube_y + radius * math.sin(math.radians(elevation))
        cam_z = 0 + radius * math.cos(math.radians(elevation)) * math.cos(math.radians(azimuth))

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        target = cubes[-1]["pos"]
        gluLookAt(cam_x, cam_y+cube_y, cam_z, target[0], target[1]+cube_y, target[2], 0, 1, 0)
        # glTranslatef(0.0, -cube_y, zoom)
        for cube in cubes:
            glPushMatrix()
            glTranslatef(*cube["pos"])
            glRotatef(cube["rot"][0], 1, 0, 0)
            glRotatef(cube["rot"][1], 0, 1, 0)
            glRotatef(cube["rot"][2], 0, 0, 1)
            draw_textured_cuboid_at(cube["pos"][0], cube["pos"][1], cube["pos"][2], 2, 2, 2)
            glPopMatrix()
        
        # cube_y += 0.05
        frame_counter += 1
        
        pygame.display.flip()
        pygame.time.wait(10)

def lose():
    quit()

game()