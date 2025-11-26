"""
Special mechanisms applied to the latest cube in the stack.
"""

import math
import random
from models import Cube


def apply_random_acceleration(
    cube: Cube,
    min_factor: float = 0.1,
    max_factor: float = 10.0
) -> None:
    """
    Apply a random acceleration to the cube's velocity, but clamp the final
    velocity magnitude between min_factor and max_factor times the original base speed.

    Parameters:
        cube (Cube): The cube to modify.
        min_factor (float): Minimum allowed speed multiplier relative to base speed.
        max_factor (float): Maximum allowed speed multiplier relative to base speed.
    """
    # Compute current velocity magnitude in XZ plane
    vx, _, vz = cube.direction
    current_speed = math.sqrt(vx**2 + vz**2)

    # Choose a random multiplier
    multiplier = random.uniform(0.5, 1.5)  # tweak range as desired
    new_speed = current_speed * multiplier

    # Clamp new speed between limits
    base_speed = cube.travel_distance / cube.travel_distance  # base = 1.0
    min_speed = base_speed * min_factor
    max_speed = base_speed * max_factor
    new_speed = max(min_speed, min(new_speed, max_speed))

    # Normalize direction and rescale to new speed
    if current_speed > 0:
        norm_x = vx / current_speed
        norm_z = vz / current_speed
        cube.direction[0] = norm_x * new_speed
        cube.direction[2] = norm_z * new_speed


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
