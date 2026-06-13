#!/usr/bin/env python3

import sys
import os
import site


def is_virtual_env() -> bool:
    """Return True if running inside a virtual environment."""
    return os.environ.get("VIRTUAL_ENV") is not None


def get_venv_name() -> str:
    """Return the name of the virtual environment."""
    return os.path.basename(sys.prefix)


def get_package_path() -> str:
    """Return the path where packages are installed."""
    paths = site.getsitepackages()
    return paths[0] if paths else "Unknown"


def show_outside() -> None:
    """Display info when running outside a virtual environment."""
    print()
    print("MATRIX STATUS: You're still plugged in")
    print()
    print(f"Current Python: {sys.executable}")
    print("Virtual Environment: None detected")
    print()
    print("WARNING: You're in the global environment!")
    print("The machines can see everything you install.")
    print()
    print("To enter the construct, run:")
    print("python -m venv matrix_env")
    print("source matrix_env/bin/activate # On Unix")
    print(r"matrix_env\Scripts\activate # On Windows")
    print()
    print("Then run this program again.")


def show_inside() -> None:
    """Display info when running inside a virtual environment."""
    print()
    print("MATRIX STATUS: Welcome to the construct")
    print()
    print(f"Current Python: {sys.executable}")
    print(f"Virtual Environment: {get_venv_name()}")
    print(f"Environment Path: {sys.prefix}")
    print()
    print("SUCCESS: You're in an isolated environment!")
    print("Safe to install packages without affecting")
    print("the global system.")
    print()
    print("Package installation path:")
    print(get_package_path())


def main() -> None:
    """Detect environment and display appropriate information."""
    if is_virtual_env():
        show_inside()
    else:
        show_outside()


if __name__ == "__main__":
    main()
