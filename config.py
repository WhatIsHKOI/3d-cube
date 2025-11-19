"""
Global configuration constants for window, assets, gameplay, and camera.
"""

# Window
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 675
DISPLAY = (SCREEN_WIDTH, SCREEN_HEIGHT)
WINDOW_TITLE = "3D Cube Stacking"

# Assets
FONT_PATH = "assets/font_pixel.ttf"
TEXTURE_PATH = "assets/cube_texture.png"
LEADERBOARD_FILE = "record.txt"

# Gameplay
INITIAL_CUBE_POS = (-1.0, -1.0, -1.0)
INITIAL_CUBE_SIZE = (2.0, 2.0, 2.0)
SPAWN_RADIUS = 10.0            # distance from target for new cube spawn
STACK_HEIGHT_STEP = 2.0        # vertical step when spawning a new cube
ARRIVAL_FRAMES = 100.0         # frames to reach target (controls speed)
MAX_DISPLAY_SCORES = 10        # number of scores stored

# Camera
INITIAL_AZIMUTH = 45.0         # degrees
INITIAL_ELEVATION = 30.0       # degrees
INITIAL_RADIUS = 10.0          # distance from focus
ELEVATION_MIN = -89.9
ELEVATION_MAX = 89.9
MOUSE_SENSITIVITY = 0.3
ZOOM_STEP = 0.5
CAMERA_Y_OFFSET = 1.0          # small lift above the cube center

# Timing
FRAME_DELAY_MS = 10
