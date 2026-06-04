#!/usr/bin/env python3

import sys
import importlib.util


def check_dependency(name: str) -> tuple[bool, str]:
    """Check if a package is installed and return version."""
    spec = importlib.util.find_spec(name)
    if spec is None:
        return (False, "not installed")
    try:
        module = __import__(name)
        version = getattr(module, "__version__", "unknown")
        return (True, version)
    except ImportError:
        return (False, "not installed")


def show_missing_instructions() -> None:
    """Show installation instructions for missing dependencies."""
    print("\nTo install dependencies:")
    print("\nUsing pip:")
    print("  pip install -r requirements.txt")
    print("\nUsing Poetry:")
    print("  poetry install")
    print("  poetry run python loading.py")


def check_all_dependencies() -> bool:
    """Check all required dependencies and return True if all present."""
    print("Checking dependencies:")
    deps = ["pandas", "numpy", "matplotlib"]
    all_ok = True
    for dep in deps:
        ok, version = check_dependency(dep)
        if ok:
            print(f"[OK] {dep} ({version})")
        else:
            print(f"[MISSING] {dep} - not installed")
            all_ok = False
    return all_ok


def run_analysis() -> None:
    """Run matrix data analysis using numpy, pandas and matplotlib."""
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt

    print("\nAnalyzing Matrix data...")
    print("Processing 1000 data points...")

    np.random.seed(42)
    data = {
        "signal": np.random.randn(1000),
        "noise": np.random.uniform(0, 1, 1000),
        "timestamp": np.arange(1000),
    }
    df = pd.DataFrame(data)

    print("Generating visualization...")
    fig, axes = plt.subplots(2, 1, figsize=(10, 6))

    axes[0].plot(df["timestamp"][:100], df["signal"][:100], color="green")
    axes[0].set_title("Matrix Signal")
    axes[0].set_xlabel("Timestamp")
    axes[0].set_ylabel("Signal")

    axes[1].hist(df["noise"], bins=30, color="green", alpha=0.7)
    axes[1].set_title("Noise Distribution")
    axes[1].set_xlabel("Value")
    axes[1].set_ylabel("Frequency")

    plt.tight_layout()
    output = "matrix_analysis.png"
    plt.savefig(output)
    plt.close()

    print("\nAnalysis complete!")
    print(f"Results saved to: {output}")


def main() -> None:
    """Main function to run the loading program."""
    print("LOADING STATUS: Loading programs...")
    print()

    all_ok = check_all_dependencies()

    if not all_ok:
        show_missing_instructions()
        sys.exit(1)

    run_analysis()


if __name__ == "__main__":
    main()
