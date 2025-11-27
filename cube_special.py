"""
Special mechanisms applied to the latest cube in the stack.
"""

import math
import random
from models import Cube


import random
from models import Cube

def teleport_forward(cube: Cube) -> None:
    """
    Teleport the cube to a random forward position along its spawn→target line,
    constrained to the direction it is currently moving.

    Parameters:
        cube (Cube): The cube to teleport.
    """
    # Current progress fraction (0 = spawn, 1 = target)
    if cube.travel_distance == 0:
        return  # avoid division by zero
    current_fraction = cube.traveled / cube.travel_distance

    # Only allow teleport further along the line (frontwards)
    if cube.moving_state == 1:
        new_fraction = random.uniform(current_fraction, min(2.0, current_fraction+0.25))
    else:
        new_fraction = random.uniform(max(0.0, current_fraction-0.25), current_fraction)
    print("teleport", new_fraction)

    # Interpolate between spawn and target
    new_x = cube.spawn[0] + new_fraction * (cube.target[0] - cube.spawn[0])
    new_y = cube.spawn[1] + new_fraction * (cube.target[1] - cube.spawn[1])
    new_z = cube.spawn[2] + new_fraction * (cube.target[2] - cube.spawn[2])

    cube.position[0] = new_x
    cube.position[1] = new_y
    cube.position[2] = new_z

    # Update traveled distance so bounce logic stays consistent
    cube.traveled = new_fraction * cube.travel_distance


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
