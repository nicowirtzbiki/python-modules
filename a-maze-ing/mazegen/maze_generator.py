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


class MazeGenerator:
    """Generate mazes using iterative recursive backtracker (DFS).

    Each cell is an int bitmask of its CLOSED walls:
    bit0=North, bit1=East, bit2=South, bit3=West.
    0xF means all four walls closed.

    Args:
        width: Number of columns (>= 2).
        height: Number of rows (>= 2).
        seed: Random seed for reproducibility (None = random).
        perfect: If True, exactly one path exists between any two cells.
    """

    _PATTERN_H: int = 7
    _PATTERN_W: int = 11  # 5 cols "4" + 1 gap + 5 cols "2"

    def __init__(
        self,
        width: int,
        height: int,
        seed: Optional[int] = None,
        perfect: bool = True,
    ) -> None:
        """Initialise the generator (does not generate yet)."""
        if width < 2 or height < 2:
            raise ValueError("Width and height must be >= 2.")
        self.width = width
        self.height = height
        self.perfect = perfect
        self.seed = seed
        self.rng = random.Random(seed)
        self.grid: list[list[int]] = []
        self.entry: tuple[int, int] = (0, 0)
        self.exit: tuple[int, int] = (width - 1, height - 1)
        self._solution: list[str] = []
        self._cells42: set[tuple[int, int]] = set()

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _in_bounds(self, row: int, col: int) -> bool:
        """Return True if (row, col) is inside the maze grid."""
        return 0 <= row < self.height and 0 <= col < self.width

    def _open_wall(self, row: int, col: int, direction: int) -> None:
        """Open the shared wall between (row,col) and its neighbour."""
        self.grid[row][col] &= ~direction
        dr, dc = DELTA[direction]
        self.grid[row + dr][col + dc] &= ~OPPOSITE[direction]

    def _42_offsets(self) -> list[tuple[int, int]]:
        """Return (row_offset, col_offset) pairs for the '42' pattern."""
        # Digit "4" — 5 cols × 7 rows
        four: list[tuple[int, int]] = [
            (0, 0), (0, 3),
            (1, 0), (1, 3),
            (2, 0), (2, 3),
            (3, 0), (3, 1), (3, 2), (3, 3), (3, 4),
            (4, 3),
            (5, 3),
            (6, 3),
        ]
        # Digit "2" — 5 cols × 7 rows, shifted 6 cols right
        two: list[tuple[int, int]] = [
            (0, 6), (0, 7), (0, 8), (0, 9), (0, 10),
            (1, 10),
            (2, 10),
            (3, 6), (3, 7), (3, 8), (3, 9), (3, 10),
            (4, 6),
            (5, 6),
            (6, 6), (6, 7), (6, 8), (6, 9), (6, 10),
        ]
        return four + two

    def _place_42(self) -> bool:
        """Stamp '42' as fully-closed cells in the maze centre.

        Returns:
            True if placed, False if maze is too small.
        """
        min_h = self._PATTERN_H + 4
        min_w = self._PATTERN_W + 4
        if self.height < min_h or self.width < min_w:
            return False

        sr = (self.height - self._PATTERN_H) // 2
        sc = (self.width - self._PATTERN_W) // 2

        cells: set[tuple[int, int]] = {
            (sr + dr, sc + dc) for dr, dc in self._42_offsets()
        }
        self._cells42 = cells
        for r, c in cells:
            self.grid[r][c] = 0xF
        return True

    def _has_3x3_open_area(self) -> bool:
        for r in range(self.height - 2):
            for c in range(self.width - 2):
                is_open = True
                for i in range(3):
                    for j in range(3):
                        cell = self.grid[r + i][c + j]
                        if i < 2 and (cell & SOUTH):
                            is_open = False
                        if j < 2 and (cell & EAST):
                            is_open = False
                if is_open:
                    return True
        return False

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def generate(
        self,
        entry: tuple[int, int],
        exit_: tuple[int, int],
    ) -> None:
        """Generate the maze with iterative DFS, then solve it.

        Args:
            entry: (x, y) coordinates of the entry cell.
            exit_: (x, y) coordinates of the exit cell.
        """
        self.entry = entry
        self.exit = exit_

        # Reset grid — all walls closed
        self.grid = [[0xF] * self.width for _ in range(self.height)]
        self._cells42 = set()

        if not self._place_42():
            print("Warning: maze too small for '42' pattern.")

        er, ec = entry[1], entry[0]
        xr, xc = exit_[1], exit_[0]
        if (er, ec) in self._cells42 or (xr, xc) in self._cells42:
            raise ValueError("Entry/exit overlaps '42' pattern.")

        # visited — 42 cells pre-marked so DFS skips them
        visited: list[list[bool]] = [
            [False] * self.width for _ in range(self.height)
        ]
        for r, c in self._cells42:
            visited[r][c] = True

        # Iterative DFS (recursive backtracker)
        visited[er][ec] = True
        stack: list[tuple[int, int]] = [(er, ec)]
        dirs = [NORTH, EAST, SOUTH, WEST]

        while stack:
            row, col = stack[-1]
            self.rng.shuffle(dirs)
            moved = False
            for d in dirs:
                dr, dc = DELTA[d]
                nr, nc = row + dr, col + dc
                if self._in_bounds(nr, nc) and not visited[nr][nc]:
                    self._open_wall(row, col, d)
                    visited[nr][nc] = True
                    stack.append((nr, nc))
                    moved = True
                    break
            if not moved:
                stack.pop()

        # Non-perfect: add random extra openings to create loops
        if not self.perfect:
            extras = max(1, (self.width * self.height) // 10)
            for _ in range(extras):
                r = self.rng.randint(0, self.height - 2)
                c = self.rng.randint(0, self.width - 2)
                d = self.rng.choice([EAST, SOUTH])
                dr, dc = DELTA[d]
                nr, nc = r + dr, c + dc
                if (r, c) not in self._cells42:
                    if (nr, nc) not in self._cells42:
                        self._open_wall(r, c, d)

        self._solution = self._solve()
        if not self._solution:
            print("Warning: no path found from entry to exit.")

    def _solve(self) -> list[str]:
        """BFS shortest path from entry to exit.

        Returns:
            List of direction chars (N/E/S/W). Empty if unreachable.
        """
        start = (self.entry[1], self.entry[0])
        end = (self.exit[1], self.exit[0])

        queue: deque[tuple[tuple[int, int], list[str]]] = deque(
            [(start, [])]
        )
        seen: set[tuple[int, int]] = {start}

        while queue:
            (row, col), path = queue.popleft()
            if (row, col) == end:
                return path
            for d in (NORTH, EAST, SOUTH, WEST):
                if not (self.grid[row][col] & d):   # wall is open
                    dr, dc = DELTA[d]
                    nxt = (row + dr, col + dc)
                    if (self._in_bounds(nxt[0], nxt[1])
                            and nxt not in seen):
                        seen.add(nxt)
                        queue.append((nxt, path + [DIR_NAME[d]]))
        return []

    def get_grid(self) -> list[list[int]]:
        """Return 2D grid of bitmask ints (closed walls per cell)."""
        return self.grid

    def get_solution(self) -> list[str]:
        """Return shortest path as list of direction chars."""
        return self._solution

    def get_42_cells(self) -> set[tuple[int, int]]:
        """Return (row, col) cells that form the '42' pattern."""
        return self._cells42
