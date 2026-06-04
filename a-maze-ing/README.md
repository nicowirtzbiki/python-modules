_This project has been created as part of the 42 curriculum by nwirtzbi, glins-ce._

## Description

A-Maze-ing generates random mazes using the **iterative recursive
backtracker (DFS)** algorithm. The maze can be perfect (unique path
between any two cells) or imperfect (extra loops). A '42' pattern is
embedded as fully-closed cells. The result is displayed in the terminal
and saved in a hex-encoded text file.

## Instructions

```bash
# Install dependencies
make install

# Run with default config
make run

# Lint
make lint

# Build the pip package (creates mazegen-1.0.0-py3-none-any.whl)
make build
```

## Config file format

| Key         | Description        | Example                |
| ----------- | ------------------ | ---------------------- |
| WIDTH       | Maze width (cols)  | `WIDTH=20`             |
| HEIGHT      | Maze height (rows) | `HEIGHT=15`            |
| ENTRY       | Entry coords x,y   | `ENTRY=0,0`            |
| EXIT        | Exit coords x,y    | `EXIT=19,14`           |
| OUTPUT_FILE | Output filename    | `OUTPUT_FILE=maze.txt` |
| PERFECT     | Unique path?       | `PERFECT=True`         |
| SEED        | Optional seed      | `SEED=42`              |

## Algorithm: Iterative Recursive Backtracker (DFS)

The maze is always built in two steps:

**Step 1 — DFS constructs a perfect maze**
Starts from the entry cell and marks it as visited. Randomly picks an
unvisited neighbour, opens the shared wall between them, and moves to
that neighbour. When stuck (no unvisited neighbours available),
backtracks to the previous cell and tries another direction. Repeats
until all cells have been visited. Because the DFS never opens a wall
towards an already visited cell, the result is always a **perfect maze**
— exactly one path exists between any two cells (a spanning tree of the
grid).

**Step 2 — Optional loops for imperfect mazes**
If `PERFECT=False`, after the DFS finishes, a number of random walls are
opened to create loops. This means multiple paths can exist between the
entry and the exit.

This algorithm is simple to implement, supports reproducibility via a
seed, and naturally produces mazes with long winding corridors.

## Reusable module

```python
from mazegen.maze_generator import MazeGenerator

gen = MazeGenerator(width=20, height=15, seed=42, perfect=True)
gen.generate(entry=(0, 0), exit_=(19, 14))

grid     = gen.get_grid()       # list[list[int]]
solution = gen.get_solution()   # list[str] e.g. ['N','E','S']
cells42  = gen.get_42_cells()   # set[tuple[int,int]]
```

Install the package: `pip install mazegen-1.0.0-py3-none-any.whl`

## Resources

- [Maze generation algorithms — Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [Jamis Buck — Maze algorithms](https://weblog.jamisbuck.org/2011/2/7/maze-generation-algorithm-recap)
- AI was used to: review type hint syntax, suggest the iterative DFS
  approach to avoid recursion limits, and help structure docstrings.
  All code was written and understood by the team.

## Team & Project Management

- **nwirtzbi** — maze generation logic: implemented the `MazeGenerator`
  class with the iterative DFS algorithm and BFS solver
  (`mazegen/maze_generator.py`).

- **glins-ce** — maze structure and visualisation: implemented the grid
  representation, '42' pattern, hex output file writer, ASCII terminal
  display, and interactive menu (`a_maze_ing.py`).

- **Planning:** We initially planned to finish the generator in the first
  week and the visualisation in the second. In practice, the '42' pattern
  and the hex output format took longer than expected, so we adjusted and
  worked on both parts in parallel towards the end.
- Tools: VS Code, Git, Claude (AI assistant)
