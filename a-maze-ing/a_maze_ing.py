#!/usr/bin/env python3
"""A-Maze-ing: maze generator and terminal visualiser.

Usage:
    python3 a_maze_ing.py config.txt
"""

import sys
import random
from typing import Any, Optional

from mazegen.maze_generator import (
    MazeGenerator,
    NORTH, EAST, SOUTH, WEST, DELTA,
)

# -----------------------------------------------------------------------
# ANSI colour helpers
# -----------------------------------------------------------------------

_RESET = "\033[0m"

_FG: dict[str, str] = {
    "white":   "\033[97m",
    "yellow":  "\033[93m",
    "cyan":    "\033[96m",
    "blue":    "\033[94m",
    "magenta": "\033[95m",
}
_BG: dict[str, str] = {
    "green":   "\033[42m",
    "red":     "\033[41m",
    "cyan":    "\033[46m",
    "magenta": "\033[45m",
}

_WALL_COLORS = ["white", "yellow", "cyan", "blue", "magenta"]


def _col(text: str, fg: str = "", bg: str = "") -> str:
    """Wrap *text* in ANSI colour codes."""
    codes = _FG.get(fg, "") + _BG.get(bg, "")
    return f"{codes}{text}{_RESET}" if codes else text


# -----------------------------------------------------------------------
# Config parsing & validation
# -----------------------------------------------------------------------

def parse_config(path: str) -> dict[str, str]:
    """Read a KEY=VALUE config file and return a string dict.

    Lines starting with '#' are ignored.

    Args:
        path: Path to the configuration file.

    Returns:
        Dict mapping config keys to their string values.
    """
    cfg: dict[str, str] = {}
    try:
        with open(path) as fh:
            for lineno, raw in enumerate(fh, 1):
                line = raw.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' not in line:
                    print(
                        f"Config error at line {lineno}: "
                        "expected KEY=VALUE"
                    )
                    sys.exit(1)
                k, v = line.split('=', 1)
                if k in cfg:
                    raise ValueError(f"{k} value is duplicated")
                cfg[k.strip()] = v.strip()
    except FileNotFoundError:
        print(f"Error: config file not found: {path}")
        sys.exit(1)
    except OSError as exc:
        print(f"Error reading config: {exc}")
        sys.exit(1)
    return cfg


def _parse_xy(raw: str, label: str) -> tuple[int, int]:
    """Parse an 'x,y' string into a tuple of ints.

    Args:
        raw: The raw string value.
        label: Name used in error messages.

    Returns:
        Tuple (x, y).

    Raises:
        ValueError on bad format.
    """
    parts = raw.split(',')
    if len(parts) != 2:
        raise ValueError(f"{label} must be 'x,y'")
    try:
        return int(parts[0].strip()), int(parts[1].strip())
    except ValueError:
        raise ValueError(f"{label} coordinates must be integers")


def validate_config(cfg: dict[str, str]) -> dict[str, Any]:
    """Validate the raw config dict and return typed parameters.

    Args:
        cfg: Raw string key-value dict from parse_config().

    Returns:
        Dict with typed values ready to use.

    Raises:
        ValueError on any invalid value.
    """
    required = ['WIDTH', 'HEIGHT', 'ENTRY', 'EXIT',
                'OUTPUT_FILE', 'PERFECT']
    for key in required:
        if key not in cfg:
            raise ValueError(f"Missing required key: {key}")
    try:
        width = int(cfg['WIDTH'])
        height = int(cfg['HEIGHT'])
    except ValueError:
        raise ValueError("WIDTH and HEIGHT must be integers")

    if width < 2 or height < 2:
        raise ValueError("WIDTH and HEIGHT must be >= 2")

    entry = _parse_xy(cfg['ENTRY'], 'ENTRY')
    exit_ = _parse_xy(cfg['EXIT'], 'EXIT')

    if not (0 <= entry[0] < width and 0 <= entry[1] < height):
        raise ValueError(f"ENTRY {entry} is out of maze bounds")
    if not (0 <= exit_[0] < width and 0 <= exit_[1] < height):
        raise ValueError(f"EXIT {exit_} is out of maze bounds")
    if entry == exit_:
        raise ValueError("ENTRY and EXIT must be different cells")

    perf_str = cfg['PERFECT'].strip().lower()
    if perf_str not in ('true', 'false'):
        raise ValueError("PERFECT must be True or False")

    seed: Optional[int] = None
    if 'SEED' in cfg:
        try:
            seed = int(cfg['SEED'])
        except ValueError:
            raise ValueError("SEED must be an integer")

    return {
        'width': width,
        'height': height,
        'entry': entry,
        'exit': exit_,
        'output_file': cfg['OUTPUT_FILE'],
        'perfect': perf_str == 'true',
        'seed': seed,
    }


# -----------------------------------------------------------------------
# Output file writer
# -----------------------------------------------------------------------

def write_output(
    filepath: str,
    grid: list[list[int]],
    entry: tuple[int, int],
    exit_: tuple[int, int],
    solution: list[str],
) -> None:
    """Write the maze to a file in the required hex format.

    Format: hex grid rows, empty line, entry coords,
    exit coords, solution path.

    Args:
        filepath: Destination path.
        grid: 2D list of cell bitmasks.
        entry: (x, y) of entry cell.
        exit_: (x, y) of exit cell.
        solution: List of direction chars.

    Raises:
        OSError on write failure.
    """
    with open(filepath, 'w') as fh:
        for row in grid:
            fh.write(''.join(format(cell, 'X') for cell in row) + '\n')
        fh.write('\n')
        fh.write(f"{entry[0]},{entry[1]}\n")
        fh.write(f"{exit_[0]},{exit_[1]}\n")
        fh.write(''.join(solution) + '\n')


# -----------------------------------------------------------------------
# ASCII renderer
# -----------------------------------------------------------------------

def _solution_cells(
    entry: tuple[int, int],
    solution: list[str],
) -> set[tuple[int, int]]:
    """Return the set of (row, col) cells on the solution path.

    Args:
        entry: Starting (x, y) cell.
        solution: List of direction chars.

    Returns:
        Set of (row, col) tuples on the path.
    """
    name_to_dir: dict[str, int] = {
        'N': NORTH, 'E': EAST, 'S': SOUTH, 'W': WEST,
    }
    cells: set[tuple[int, int]] = set()
    r, c = entry[1], entry[0]
    cells.add((r, c))
    for ch in solution:
        dr, dc = DELTA[name_to_dir[ch]]
        r, c = r + dr, c + dc
        cells.add((r, c))
    return cells


def render(
    grid: list[list[int]],
    entry: tuple[int, int],
    exit_: tuple[int, int],
    show_path: bool,
    solution: list[str],
    cells42: set[tuple[int, int]],
    wall_color: str,
) -> None:
    """Clear the terminal and print the maze as coloured ASCII art.

    Walls are drawn with + - | characters. Special cells:
    S = entry (green), E = exit (red), 42-pattern (magenta),
    solution path (cyan).

    Args:
        grid: 2D list of cell bitmasks.
        entry: (x, y) of entry.
        exit_: (x, y) of exit.
        show_path: Whether to highlight the solution.
        solution: Solution direction chars.
        cells42: Cells belonging to the '42' pattern.
        wall_color: Colour name for wall characters.
    """
    h = len(grid)
    w = len(grid[0])
    wc = _FG.get(wall_color, _FG["white"])

    path: set[tuple[int, int]] = set()
    if show_path:
        path = _solution_cells(entry, solution)

    def wall(ch: str) -> str:
        """Return a wall character with the chosen colour."""
        return f"{wc}{ch}{_RESET}"

    print("\033[2J\033[H", end="")   # clear screen, cursor home

    for row in range(h):
        top_line = ""
        mid_line = ""
        for col in range(w):
            cell = grid[row][col]

            top_line += wall("+")
            top_line += wall("--") if (cell & NORTH) else "  "

            mid_line += wall("|") if (cell & WEST) else " "

            pos = (row, col)
            if pos == (entry[1], entry[0]):
                mid_line += _col("S ", bg="green")
            elif pos == (exit_[1], exit_[0]):
                mid_line += _col("E ", bg="red")
            elif pos in cells42:
                mid_line += _col("42", bg="magenta")
            elif show_path and pos in path:
                mid_line += _col("  ", bg="cyan")
            else:
                mid_line += "  "

        top_line += wall("+")
        last_cell = grid[row][w - 1]
        mid_line += wall("|") if (last_cell & EAST) else " "

        print(top_line)
        print(mid_line)

    # Bottom border
    bottom = ""
    for col in range(w):
        bottom += wall("+")
        bottom += wall("--") if (grid[h - 1][col] & SOUTH) else "  "
    bottom += wall("+")
    print(bottom)


# -----------------------------------------------------------------------
# Generator factory
# -----------------------------------------------------------------------

def _make_gen(params: dict[str, Any], seed: Optional[int]) -> MazeGenerator:
    """Create and run a MazeGenerator with the given seed.

    Args:
        params: Validated config dict.
        seed: Seed to use.

    Returns:
        A fully generated MazeGenerator instance.
    """
    gen = MazeGenerator(
        width=params['width'],
        height=params['height'],
        seed=seed,
        perfect=params['perfect'],
    )
    try:
        gen.generate(
                entry=params['entry'],
                exit_=params['exit'],
                )
        return gen
    except Exception as e:
        print(e)
        sys.exit(1)


# -----------------------------------------------------------------------
# Interactive loop
# -----------------------------------------------------------------------

def run(params: dict[str, Any]) -> None:
    """Main interactive display loop.

    Args:
        params: Validated config dict.
    """
    wall_idx = 0
    show_path = False
    seed: int = (
        params['seed']
        if params['seed'] is not None
        else random.randint(0, 10 ** 9)
    )

    gen = _make_gen(params, seed)

    try:
        write_output(
            params['output_file'],
            gen.get_grid(),
            params['entry'],
            params['exit'],
            gen.get_solution(),
        )
    except OSError as exc:
        print(f"Error writing output: {exc}")
        sys.exit(1)

    while True:
        render(
            gen.get_grid(),
            params['entry'],
            params['exit'],
            show_path,
            gen.get_solution(),
            gen.get_42_cells(),
            _WALL_COLORS[wall_idx],
        )
        print("\n==== A-Maze-ing ====")
        if not gen.get_42_cells():
            print(
                _col("Warning: maze too small for '42' pattern.", fg="yellow")
            )
        print("1. Re-generate a new maze")
        print("2. Show/Hide solution path")
        print("3. Rotate wall colour")
        print("4. Quit")
        choice = input("Choice (1-4): ").strip()

        if choice == '1':
            seed = random.randint(0, 10 ** 9)
            gen = _make_gen(params, seed)
            try:
                write_output(
                    params['output_file'],
                    gen.get_grid(),
                    params['entry'],
                    params['exit'],
                    gen.get_solution(),
                )
            except OSError as exc:
                print(f"Error writing output: {exc}")
        elif choice == '2':
            show_path = not show_path
        elif choice == '3':
            wall_idx = (wall_idx + 1) % len(_WALL_COLORS)
        elif choice == '4':
            print("Bye!")
            break
        else:
            input("Invalid choice. Press Enter to continue...")


# -----------------------------------------------------------------------
# Entry point
# -----------------------------------------------------------------------

def main() -> None:
    """Entry point — parse args, load config, start loop."""
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        sys.exit(1)

    try:
        raw = parse_config(sys.argv[1])
        params = validate_config(raw)
        run(params)
    except ValueError as exc:
        print(f"Config error: {exc}")
        sys.exit(1)
    except (KeyboardInterrupt, EOFError) as e:
        print(e)
        sys.exit(0)


if __name__ == "__main__":
    main()
