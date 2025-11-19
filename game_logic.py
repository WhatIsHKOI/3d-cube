"""
Core gameplay logic: intersection, stopping, trimming, and spawning cubes.
"""

import math
import random
from typing import Optional, Tuple, List
from models import Cube
from config import SPAWN_RADIUS, STACK_HEIGHT_STEP, ARRIVAL_FRAMES


def intersect_rect(r1: Tuple[float, float, float, float],
                   r2: Tuple[float, float, float, float]) -> Optional[Tuple[float, float, float, float]]:
    """
    Compute intersection of two axis-aligned rectangles in XZ plane.

    Parameters:
        r1 (Tuple[float, float, float, float]): (x, z, width, depth) of first rectangle.
        r2 (Tuple[float, float, float, float]): (x, z, width, depth) of second rectangle.

    Returns:
        Optional[Tuple[float, float, float, float]]: (x, z, width, depth) of overlap or None.
    """
    x1, z1, w1, d1 = r1
    x2, z2, w2, d2 = r2

    left = max(x1, x2)
    right = min(x1 + w1, x2 + w2)
    back = max(z1, z2)
    front = min(z1 + d1, z2 + d2)

    if left < right and back < front:
        return (left, back, right - left, front - back)
    return None


def trim_or_lose(stack: List[Cube]) -> bool:
    """
    Trim the top moving cube based on intersection with the previous cube.
    If no intersection, signal loss.

    Parameters:
        stack (List[Cube]): Current stack of cubes.

    Returns:
        bool: True if player loses (no overlap), False otherwise.
    """
    if len(stack) < 2:
        return False

    prev = stack[-2]
    curr = stack[-1]

    r1 = (prev.position[0], prev.position[2], prev.size[0], prev.size[2])
    r2 = (curr.position[0], curr.position[2], curr.size[0], curr.size[2])
    overlap = intersect_rect(r1, r2)

    if overlap is None:
        return True

    ox, oz, ow, od = overlap
    curr.position[0] = ox
    curr.position[2] = oz
    curr.size[0] = ow
    curr.size[2] = od
    return False


def spawn_next_cube(stack: List[Cube]) -> None:
    """
    Spawn a new moving cube around the target position of the last cube.

    Parameters:
        stack (List[Cube]): Current stack of cubes.
    """
    base = stack[-1]
    target_x, target_z = base.position[0], base.position[2]

    angle = random.uniform(-math.pi, math.pi)
    spawn_x = target_x + SPAWN_RADIUS * math.cos(angle)
    spawn_z = target_z + SPAWN_RADIUS * math.sin(angle)
    spawn_y = base.position[1] + STACK_HEIGHT_STEP

    dx = target_x - spawn_x
    dz = target_z - spawn_z
    direction = [dx / ARRIVAL_FRAMES, 0.0, dz / ARRIVAL_FRAMES]
    travel_distance = math.sqrt(dx**2 + dz**2)

    new_cube = Cube(
        position=[spawn_x, spawn_y, spawn_z],
        rotation=base.rotation[:],
        size=base.size[:],
        direction=direction,
        moving_state=1,
        spawn=[spawn_x, spawn_y, spawn_z],
        target=[target_x, spawn_y, target_z],
        travel_distance=travel_distance,
        traveled=0.0
    )
    stack.append(new_cube)


def stop_and_spawn(stack: List[Cube]) -> bool:
    """
    Stop the current moving cube, apply trimming, and spawn the next cube.

    Parameters:
        stack (List[Cube]): Current stack of cubes.

    Returns:
        bool: True if player loses (no overlap), False otherwise.
    """
    stack[-1].moving_state = 0
    did_lose = trim_or_lose(stack)
    if not did_lose:
        spawn_next_cube(stack)
    return did_lose
