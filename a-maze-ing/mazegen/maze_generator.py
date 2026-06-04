"""Maze generation module — reusable as a pip package.

Usage::

    from mazegen.maze_generator import MazeGenerator

    gen = MazeGenerator(width=20, height=15, seed=42, perfect=True)
    gen.generate(entry=(0, 0), exit_=(19, 14))

    grid     = gen.get_grid()       # list[list[int]]
    solution = gen.get_solution()   # list[str] e.g. ['N', 'E', 'S']
    cells42  = gen.get_42_cells()   # set[tuple[int, int]] (row, col)
"""

import random
from collections import deque
from typing import Optional

# Wall bitmask constants — bit set = wall CLOSED
NORTH: int = 1   # bit 0
EAST: int = 2    # bit 1
SOUTH: int = 4   # bit 2
WEST: int = 8    # bit 3

OPPOSITE: dict[int, int] = {
    NORTH: SOUTH,
    SOUTH: NORTH,
    EAST: WEST,
    WEST: EAST,
}

DELTA: dict[int, tuple[int, int]] = {
    NORTH: (-1, 0),
    SOUTH: (1, 0),
    EAST: (0, 1),
    WEST: (0, -1),
}

DIR_NAME: dict[int, str] = {
    NORTH: 'N', EAST: 'E', SOUTH: 'S', WEST: 'W',
}


