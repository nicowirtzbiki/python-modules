#!/usr/bin/env python3

import sys
import typing


def open_file(filename: str) -> None:
    """
    Opens a file and displays its contents.
    Handles FileNotFoundError and PermissionError via OSError.
    The open() function returns a typing.IO object.
    """
    try:
        print(f"Accessing file '{filename}'")
        f: typing.IO = open(filename)
        print("---")
        print()
        content = f.read()
        print(content)
        print()
        print("---")
        f.close()
        print(f"File '{filename}' closed.")
    except OSError as err:
        print(f"Error opening file '{filename}': {err}")
        return


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: ft_ancient_text.py <file>")
        sys.exit(1)
    print("=== Cyber Archives Recovery ===")
    open_file(sys.argv[1])
