#!/usr/bin/env python3

import sys
import typing


def print_content(content: str) -> None:
    """
    Prints the content of a file with formatting.
    """
    print("---")
    print()
    print(content)
    print()
    print("---")


def transform_content(content: str) -> str:
    """Adds # at the end of each line."""
    lines = content.split("\n")
    new_lines = [line + "#" for line in lines if line != ""]
    return "\n".join(new_lines)


def open_file(filename: str) -> str:
    """Opens a file, displays and returns its contents."""
    try:
        print(f"Accessing file '{filename}'")
        f: typing.IO = open(filename)
        content = f.read()
        print_content(content)
        f.close()
        print(f"File '{filename}' closed.")
        return content
    except OSError as err:
        print(f"Error opening file '{filename}': {err}")
        return ""

def write_file(filename: str, content: str) -> None:
    """Writes content to a file."""
    try:
        f: typing.IO = open(filename, "w")
        f.write(content)
        f.close()
        print(f"Data saved in file '{filename}'.")
    except OSError as err:
        print(f"Error saving file '{filename}': {err}")


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: ft_archive_creation.py <file>")
        sys.exit(1)
    print("=== Cyber Archives Recovery & Preservation ===")
    content = open_file(sys.argv[1])
    if content == "":
        return
    print()
    print("Transform data:")
    new_content = transform_content(content)
    print_content(new_content)
    filename = input("Enter new file name (or empty): ")
    if filename == "":
        print("Not saving data.")
    else:
        print(f"Saving data to '{filename}'")
        write_file(filename, new_content)


if __name__ == "__main__":
    main()