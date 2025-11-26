"""
Main game loop: input handling, camera control, cube movement, and rendering.
"""

import math
import time
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import DOUBLEBUF, OPENGL

from models import Cube
from cube_special import apply_random_acceleration, apply_random_rotation
from graphics import load_texture, draw_textured_cuboid
from game_logic import spawn_next_cube, stop_and_spawn
from leaderboard import update_leaderboard
from hud import draw_hud_text
from lose_screen import lose_screen
from config import (
    DISPLAY, SCREEN_WIDTH, SCREEN_HEIGHT,
    INITIAL_CUBE_POS, INITIAL_CUBE_SIZE,
    INITIAL_AZIMUTH, INITIAL_ELEVATION, INITIAL_RADIUS,
    ELEVATION_MIN, ELEVATION_MAX, MOUSE_SENSITIVITY,
    ZOOM_STEP, CAMERA_Y_OFFSET, FRAME_DELAY_MS,
    LEADERBOARD_FILE, textures
)


def compute_camera_position(azimuth: float, elevation: float, radius: float,
                            focus_x: float, focus_y: float, focus_z: float,
                            y_lift: float = 0.0) -> tuple:
    """
    Compute camera position and target based on spherical coords and focus point.

    Parameters:
        azimuth (float): Horizontal angle in degrees.
        elevation (float): Vertical angle in degrees.
        radius (float): Distance from focus point.
        focus_x (float): Focus x coordinate.
        focus_y (float): Focus y coordinate.
        focus_z (float): Focus z coordinate.
        y_lift (float): Additional vertical offset for camera and target.

    Returns:
        tuple: (cam_x, cam_y, cam_z, tar_x, tar_y, tar_z)
    """
    cam_x = focus_x + radius * math.cos(math.radians(elevation)) * math.sin(math.radians(azimuth))
    cam_y = focus_y + y_lift + radius * math.sin(math.radians(elevation))
    cam_z = focus_z + radius * math.cos(math.radians(elevation)) * math.cos(math.radians(azimuth))
    tar_x, tar_y, tar_z = focus_x, focus_y + y_lift, focus_z
    return cam_x, cam_y, cam_z, tar_x, tar_y, tar_z


def update_cube_motion(active: Cube) -> None:
    """
    Update active cube position and bounce behavior.

    Parameters:
        active (Cube): The currently moving cube.
    """
    step = active.step_distance()

    if active.moving_state == 1:  # forward
        active.position[0] += active.direction[0]
        active.position[1] += active.direction[1]
        active.position[2] += active.direction[2]
        active.traveled += step
        if active.traveled >= 2 * active.travel_distance:
            active.moving_state = 2

    elif active.moving_state == 2:  # backward
        active.position[0] -= active.direction[0]
        active.position[1] -= active.direction[1]
        active.position[2] -= active.direction[2]
        active.traveled -= step
        if active.traveled <= 0:
            active.moving_state = 1


def game_loop(main_menu_callback) -> None:
    """
    Run the main game loop.

    Parameters:
        on_game_over_callback (function): Called when player loses, with score as argument.
    """
    pygame.display.set_mode(DISPLAY, DOUBLEBUF | OPENGL)

    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, SCREEN_WIDTH / SCREEN_HEIGHT, 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)

    # Load textures
    for name, file in textures.items():
        textures[name] = None
    for name, file in textures.items():
        if file is None:
            textures[name] = load_texture("assets/textures/"+name+".png")

    # Camera
    azimuth = INITIAL_AZIMUTH
    elevation = INITIAL_ELEVATION
    radius = INITIAL_RADIUS
    dragging = False
    last_mouse_pos = None
    vertical_offset = 0.0
    frame_counter = 0

    # Stack initialization
    stack = [
        Cube(
            position=list(INITIAL_CUBE_POS),
            rotation=[0.0, 0.0, 0.0],
            size=list(INITIAL_CUBE_SIZE),
            moving_state=0
        )
    ]
    spawn_next_cube(stack)

    last_second = time.time()
    is_running = True
    while is_running:
        current_time = time.time()
        if current_time - last_second >= 1.0:
            last_second = current_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                dragging = True
                last_mouse_pos = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    dragging = False
                elif event.button == 4:
                    radius = max(2.0, radius - ZOOM_STEP)
                elif event.button == 5:
                    radius = min(50.0, radius + ZOOM_STEP)

            if event.type == pygame.MOUSEMOTION and dragging:
                x, y = pygame.mouse.get_pos()
                mdx = x - last_mouse_pos[0]
                mdy = y - last_mouse_pos[1]
                azimuth -= mdx * MOUSE_SENSITIVITY
                elevation = max(ELEVATION_MIN, min(ELEVATION_MAX, elevation + mdy * MOUSE_SENSITIVITY))
                last_mouse_pos = (x, y)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                did_lose = stop_and_spawn(stack)
                if did_lose:
                    score = len(stack) - 2
                    update_leaderboard(score, LEADERBOARD_FILE)
                    lose_screen(score, restart_callback=game_loop, menu_callback=main_menu_callback)
                    return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            quit()
        if keys[pygame.K_w]:
            vertical_offset += 0.1
        if keys[pygame.K_s]:
            vertical_offset -= 0.1

        # Update motion
        active = stack[-1]
        if active.moving_state in (1, 2):
            update_cube_motion(active)

        # Update for special cubes
        if active.texture_id == "var_a" and frame_counter % 40 == 0:
            apply_random_acceleration(active, -0.15, 3.0)
        if active.texture_id == "var_sz" and frame_counter % 40 == 0:
            apply_random_acceleration(active, -0.25, 7.5)

        # Camera focus
        focus_cube = stack[-2] if len(stack) >= 2 else stack[-1]
        focus_x = focus_cube.position[0] + focus_cube.size[0] / 2.0
        focus_y = focus_cube.position[1] + focus_cube.size[1] / 2.0 + vertical_offset
        focus_z = focus_cube.position[2] + focus_cube.size[2] / 2.0

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        cam_x, cam_y, cam_z, tar_x, tar_y, tar_z = compute_camera_position(
            azimuth, elevation, radius, focus_x, focus_y, focus_z, y_lift=CAMERA_Y_OFFSET
        )
        gluLookAt(cam_x, cam_y, cam_z, tar_x, tar_y, tar_z, 0, 1, 0)

        # Draw cubes
        for cube in stack:
            glPushMatrix()
            glTranslatef(*cube.position)
            glRotatef(cube.rotation[0], 1, 0, 0)
            glRotatef(cube.rotation[1], 0, 1, 0)
            glRotatef(cube.rotation[2], 0, 0, 1)
            draw_textured_cuboid(tuple(cube.size), cube.texture_id)
            glPopMatrix()

        # HUD overlay (score)
        score = len(stack) - 2
        draw_hud_text(f"Score: {score}", 20, SCREEN_HEIGHT - 40)

        frame_counter = frame_counter+1

        pygame.display.flip()
        pygame.time.wait(FRAME_DELAY_MS)
