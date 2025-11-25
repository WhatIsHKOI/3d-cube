"""
Core game models and structures.
"""

from dataclasses import dataclass, field
from typing import List, Tuple


@dataclass
class Cube:
    """
    Represents a single cube in the stack with position, rotation, size,
    movement state, and precomputed travel properties.

    Attributes:
        position (List[float]): [x, y, z] position in world space.
        rotation (List[float]): [rx, ry, rz] rotation angles in degrees.
        size (List[float]): [width, height, depth] dimensions.
        direction (List[float]): per-frame movement delta [dx, dy, dz].
        moving_state (int): 0=stopped, 1=forward, 2=backward.
        spawn (List[float]): spawn position [x, y, z].
        target (List[float]): target position [x, y, z].
        travel_distance (float): straight-line distance from spawn to target.
        traveled (float): accumulated distance traveled along the path.
        texture_id: which texture is used to render this cube in the following list:
            0 - normal cube
            1 - cube with variable acceleration
    """
    position: List[float]
    rotation: List[float]
    size: List[float]
    direction: List[float] = field(default_factory=lambda: [0.0, 0.0, 0.0])
    moving_state: int = 0
    spawn: List[float] = field(default_factory=lambda: [0.0, 0.0, 0.0])
    target: List[float] = field(default_factory=lambda: [0.0, 0.0, 0.0])
    travel_distance: float = 0.0
    traveled: float = 0.0
    texture_id: str = "normal"

    def step_distance(self) -> float:
        """
        Compute the per-frame horizontal distance of movement.

        Returns:
            float: Euclidean distance for current direction in XZ plane.
        """
        dx, _, dz = self.direction
        return (dx**2 + dz**2) ** 0.5
