"""
Special mechanisms applied to the latest cube in the stack.
"""

import random
from models import Cube


def apply_random_acceleration(cube: Cube, min_accel: float = -0.01, max_accel: float = 0.01) -> None:
    """
    Apply a random acceleration to the latest cube's direction vector.

    Parameters:
        cube (Cube): The cube to modify.
        min_accel (float): Minimum acceleration magnitude.
        max_accel (float): Maximum acceleration magnitude.
    """
    accel = random.uniform(min_accel, max_accel)

    # Apply acceleration along the cube's movement direction
    cube.direction[0] *= (1.0 + accel)
    cube.direction[2] *= (1.0 + accel)


def apply_random_rotation(cube: Cube, max_angle: float = 5.0) -> None:
    """
    Apply a small random rotation to the latest cube.

    Parameters:
        cube (Cube): The cube to modify.
        max_angle (float): Maximum rotation angle in degrees.
    """
    cube.rotation[0] += random.uniform(-max_angle, max_angle)
    cube.rotation[1] += random.uniform(-max_angle, max_angle)
    cube.rotation[2] += random.uniform(-max_angle, max_angle)
