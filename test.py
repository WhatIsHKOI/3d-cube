import math
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random
import time

#Initialization
pygame.init()
screen_width = 1200
screen_height = 675
display = (screen_width, screen_height)
pygame.display.set_caption("3d cube stacking")

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

def intersect_rect(r1, r2):
    # r1 and r2 are tuples: (x, z, width, depth)
    x1, z1, w1, d1 = r1
    x2, z2, w2, d2 = r2

    left = max(x1, x2)
    right = min(x1 + w1, x2 + w2)
    back = max(z1, z2)
    front = min(z1 + d1, z2 + d2)

    if left < right and back < front:
        return (left, back, right - left, front - back)
    else:
        return None

def draw_textured_cuboid_at(x, y, z, width, height, depth, texture_id):
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glBegin(GL_QUADS)

    # Offset and scale vertices — REMOVE the position offset here
    def V(v): return (v[0] * width, v[1] * height, v[2] * depth)

    # Define cuboid faces
    face_vertices = [
        (V((0.0, 0.0, 0.0)), V((1.0, 0.0, 0.0)), V((1.0, 1.0, 0.0)), V((0.0, 1.0, 0.0))),  # Back
        (V((0.0, 0.0, 1.0)), V((1.0, 0.0, 1.0)), V((1.0, 1.0, 1.0)), V((0.0, 1.0, 1.0))),  # Front
        (V((0.0, 0.0, 0.0)), V((1.0, 0.0, 0.0)), V((1.0, 0.0, 1.0)), V((0.0, 0.0, 1.0))),  # Bottom
        (V((0.0, 1.0, 0.0)), V((1.0, 1.0, 0.0)), V((1.0, 1.0, 1.0)), V((0.0, 1.0, 1.0))),  # Top
        (V((1.0, 0.0, 0.0)), V((1.0, 1.0, 0.0)), V((1.0, 1.0, 1.0)), V((1.0, 0.0, 1.0))),  # Right
        (V((0.0, 0.0, 0.0)), V((0.0, 1.0, 0.0)), V((0.0, 1.0, 1.0)), V((0.0, 0.0, 1.0))),  # Left
    ]

    tex_coords = [(0, 0), (1, 0), (1, 1), (0, 1)]

    for face in face_vertices:
        for i in range(4):
            glTexCoord2fv(tex_coords[i])
            glVertex3fv(face[i])
    glEnd()

def draw_text_in_box(screen, text, box, size=32, color=(255,255,255), align="left"):
    """
    Draw text inside a rectangular box using Pygame blit.
    box = (x1, y1, x2, y2) with top-left origin.
    align = 'left', 'center', or 'right'.
    """
    font = pygame.font.Font("assets/font_pixel.ttf", size)
    text_surface = font.render(text, True, color)
    w, h = text_surface.get_size()

    x1, y1, x2, y2 = box
    box_w = x2 - x1
    box_h = y2 - y1

    # Vertical placement: top of box (could extend with valign if needed)
    y = y1

    # Horizontal placement depends on align
    if align == "left":
        x = x1
    elif align == "center":
        x = x1 + (box_w - w) // 2
    elif align == "right":
        x = x2 - w
    else:
        x = x1

    # Blit text surface onto screen
    screen.blit(text_surface, (x, y))

def main():

    screen = pygame.display.set_mode(display)
    running = 1
    while running:

        screen.fill((0, 0, 0))
        draw_text_in_box(screen, "Press SPACE to start", (screen_width//2-200, screen_height//2-100, screen_width//2+200, screen_height//2), size=32, align="center")
        draw_text_in_box(screen, "Press ESC to quit game", (screen_width//2-200, screen_height//2, screen_width//2+200, screen_height//2+100), size=32, align="center")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            keys = pygame.key.get_pressed()
            if (keys[K_SPACE]):
                game()
                quit()
            elif (keys[K_ESCAPE]):
                quit()

        pygame.display.flip()
    
    quit()

import math, random

def stop_and_spawn_cube(cubes, frame_counter):
    """
    Stops the current cube, trims it if needed, and spawns a new cube.
    Each cube stores its spawn position, target position, direction vector,
    travel distance, and traveled distance.
    """

    # Stop the current cube
    cubes[-1]["moving"] = 0

    # Intersection check if at least 2 cubes
    if len(cubes) >= 2:
        r1 = (cubes[-2]["pos"][0], cubes[-2]["pos"][2],
              cubes[-2]["size"][0], cubes[-2]["size"][2])
        r2 = (cubes[-1]["pos"][0], cubes[-1]["pos"][2],
              cubes[-1]["size"][0], cubes[-1]["size"][2])
        intersection = intersect_rect(r1, r2)

        if intersection is None:
            lose()
            return cubes, frame_counter
        else:
            ix, iz, iw, id = intersection
            cubes[-1]["pos"][0] = ix
            cubes[-1]["pos"][2] = iz
            cubes[-1]["size"][0] = iw
            cubes[-1]["size"][2] = id

    else:
        frame_counter = 0

    # --- Spawn new cube ---
    spawn_angle = random.uniform(-math.pi, math.pi)

    target_x = cubes[-1]["pos"][0]
    target_z = cubes[-1]["pos"][2]

    spawn_x = target_x + 10.0 * math.cos(spawn_angle)
    spawn_z = target_z + 10.0 * math.sin(spawn_angle)
    spawn_y = cubes[-1]["pos"][1] + 2.0

    dx = target_x - spawn_x
    dz = target_z - spawn_z

    # Arrival frame controls speed
    arrival_frame = 100.0
    direction = [dx / arrival_frame, 0.0, dz / arrival_frame]

    # Compute straight-line travel distance
    travel_distance = math.sqrt(dx**2 + dz**2)

    new_cube = {
        "pos": [spawn_x, spawn_y, spawn_z],
        "rot": cubes[-1]["rot"][:],
        "size": cubes[-1]["size"][:],
        "target": [target_x, spawn_y, target_z],
        "direction": direction,
        "moving": 1,
        "spawn": [spawn_x, spawn_y, spawn_z],
        "travel_distance": travel_distance,
        "traveled": 0.0
    }
    cubes.append(new_cube)

    return cubes, frame_counter

def game():

    # OpenGL setup
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)
    zoom = -5.0
    glTranslatef(0.0, 0.0, zoom)
    texture_id = load_texture("assets/cube_texture.png")

    # Main game
    running = 1
    dragging = False
    last_mouse_pos = None
    second_counter = time.time()
    cube_y = 0
    azimuth = 45.0      # Horizontal angle (left/right)
    elevation = 30.0   # Vertical angle (up/down)
    radius = 10.0      # Distance from target (zoom)
    frame_counter = 0 # Debug use

    # Cube data structure
    cubes = [{
        "pos": [-1.0, -1.0, -1.0],
        "rot": [0.0, 0.0, 0.0],
        "size": [2.0, 2.0, 2.0],
        "moving": 0,
        "dx": 0,
        "dz": 0,
    }]
    stop_and_spawn_cube(cubes, frame_counter)

    while running:

        # Each frame initialize variables
        x_angle = 0
        y_angle = 0
        z_angle = 0
        current_time = time.time()

        if current_time - second_counter >= 1.0:
            print("1 second passed", frame_counter)
            second_counter = current_time

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    dragging = True
                    last_mouse_pos = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    dragging = False
                elif event.button == 4:  # Scroll up
                    radius -= 0.5  # Zoom in
                elif event.button == 5:  # Scroll down
                    radius += 0.5  # Zoom out

            if event.type == pygame.MOUSEMOTION and dragging:
                x, y = pygame.mouse.get_pos()
                mdx = x - last_mouse_pos[0]
                mdy = y - last_mouse_pos[1]
                
                azimuth -= mdx * 0.3
                elevation += mdy * 0.3
                elevation = max(-89.9, min(89.9, elevation))  # Clamp to avoid gimbal lock

                last_mouse_pos = (x, y)
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    space_pressed = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    stop_and_spawn_cube(cubes, frame_counter)

        keys = pygame.key.get_pressed()
        if keys[K_ESCAPE]:
            pygame.quit()
            quit()
        
        # print("new cube", cubes[-1]["moving"], frame_counter, len(cubes))
        if keys[K_w]:
            cube_y += 0.1  # Move camera up
        if keys[K_s]:
            cube_y -= 0.1  # Move camera down

        # Update cube movement
        if cubes[-1]["moving"] == 1:   # moving forward
            cubes[-1]["pos"][0] += cubes[-1]["direction"][0]
            cubes[-1]["pos"][1] += cubes[-1]["direction"][1]
            cubes[-1]["pos"][2] += cubes[-1]["direction"][2]

            # accumulate traveled distance
            step = math.sqrt(cubes[-1]["direction"][0]**2 + cubes[-1]["direction"][2]**2)
            cubes[-1]["traveled"] += step

            # reverse after twice the spawn-to-target distance
            if cubes[-1]["traveled"] >= 2 * cubes[-1]["travel_distance"]:
                cubes[-1]["moving"] = 2

        elif cubes[-1]["moving"] == 2:  # moving backward
            cubes[-1]["pos"][0] -= cubes[-1]["direction"][0]
            cubes[-1]["pos"][1] -= cubes[-1]["direction"][1]
            cubes[-1]["pos"][2] -= cubes[-1]["direction"][2]

            cubes[-1]["traveled"] -= step

            if cubes[-1]["traveled"] <= 0:
                cubes[-1]["moving"] = 1

        # print("counter", counter, 2*abs(dx))

        
        cubes[-1]["rot"][0] = (cubes[-1]["rot"][0] + x_angle + 360) % 360
        cubes[-1]["rot"][1] = (cubes[-1]["rot"][1] + y_angle + 360) % 360
        cubes[-1]["rot"][2] = (cubes[-1]["rot"][2] + z_angle + 360) % 360

        cam_x = 0 + radius * math.cos(math.radians(elevation)) * math.sin(math.radians(azimuth))
        cam_y = cube_y + radius * math.sin(math.radians(elevation))
        cam_z = 0 + radius * math.cos(math.radians(elevation)) * math.cos(math.radians(azimuth))

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        if len(cubes) == 1:
            top_cube = cubes[-1]
        else:
            top_cube = cubes[-2]
        center_x = top_cube["pos"][0] + top_cube["size"][0] / 2.0
        center_y = top_cube["pos"][1] + top_cube["size"][1] / 2.0
        center_z = top_cube["pos"][2] + top_cube["size"][2] / 2.0

        gluLookAt(cam_x, cam_y + center_y + cube_y + 1.0, cam_z, center_x, center_y + cube_y + 1.0, center_z, 0, 1, 0)

        # glTranslatef(0.0, -cube_y, zoom)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        for cube in cubes:
            glPushMatrix()
            glTranslatef(*cube["pos"])
            glRotatef(cube["rot"][0], 1, 0, 0)
            glRotatef(cube["rot"][1], 0, 1, 0)
            glRotatef(cube["rot"][2], 0, 0, 1)
            draw_textured_cuboid_at(cube["pos"][0], cube["pos"][1], cube["pos"][2], cube["size"][0], cube["size"][1], cube["size"][2], texture_id)
            glPopMatrix()
        
        # cube_y += 0.05
        frame_counter += 1
        
        pygame.display.flip()
        pygame.time.wait(10)

def lose():

    screen = pygame.display.set_mode(display)
    running = 1
    while running:

        screen.fill((0, 0, 0))
        draw_text_in_box(screen, "You Lose! Press SPACE to restart", (screen_width//2-200, screen_height//2-100, screen_width//2+200, screen_height//2), size=32, align="center")
        draw_text_in_box(screen, "Press ESC to quit game", (screen_width//2-200, screen_height//2, screen_width//2+200, screen_height//2+100), size=32, align="center")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            keys = pygame.key.get_pressed()
            if (keys[K_SPACE]):
                game()
                quit()
            elif (keys[K_ESCAPE]):
                quit()

        pygame.display.flip()
    
    quit()

main()