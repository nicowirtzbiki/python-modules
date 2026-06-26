#!/usr/bin/env python3

import functools
import operator
from collections.abc import Callable
from typing import Any


def spell_reducer(spells: list[int], operation: str) -> int:
    """Reduce spell powers using functools.reduce."""
    if not spells:
        return 0

    operations: dict[str, Callable] = {
        "add": operator.add,
        "multiply": operator.mul,
        "max": max,
        "min": min,
    }

    if operation not in operations:
        print(f"Unknown operation: {operation}")
        return 0

    try:
        if operation in ("max", "min"):
            return operations[operation](spells)
        return functools.reduce(operations[operation], spells)
    except Exception as e:
        print(f"Reducer error: {e}")
        return 0


def partial_enchanter(base_enchantment: Callable) -> dict[str, Callable]:
    """Create partial applications of base enchantment."""
    return {
        "fire": functools.partial(
            base_enchantment, power=50, element="fire"
        ),
        "ice": functools.partial(
            base_enchantment, power=50, element="ice"
        ),
        "lightning": functools.partial(
            base_enchantment, power=50, element="lightning"
        ),
    }


@functools.lru_cache(maxsize=None)
def memoized_fibonacci(n: int) -> int:
    """Calculate fibonacci number with memoization."""
    if n < 0:
        raise ValueError("n must be non-negative")
    if n <= 1:
        return n
    return memoized_fibonacci(n - 1) + memoized_fibonacci(n - 2)


def spell_dispatcher() -> Callable[[Any], str]:
    """Create single dispatch spell system."""

    @functools.singledispatch
    def cast_spell(arg: Any) -> str:
        """Handle unknown spell type."""
        return "Unknown spell type"

    @cast_spell.register(int)
    def _(arg: int) -> str:
        """Handle damage spell."""
        return f"Damage spell: {arg} damage"

    @cast_spell.register(str)
    def _(arg: str) -> str:
        """Handle enchantment spell."""
        return f"Enchantment: {arg}"

    @cast_spell.register(list)
    def _(arg: list) -> str:
        """Handle multi-cast spell."""
        return f"Multi-cast: {len(arg)} spells"

    return cast_spell


def base_enchantment(power: int, element: str, target: str) -> str:
    """Base enchantment function."""
    return f"{element.capitalize()} {target} with {power} power"


def main() -> None:
    """Test all functools functions."""
    try:
        print()
        print("Testing spell reducer...")
        spells = [10, 20, 30, 40]
        print(f"Sum: {spell_reducer(spells, 'add')}")
        print(f"Product: {spell_reducer(spells, 'multiply')}")
        print(f"Max: {spell_reducer(spells, 'max')}")
        print()

        print("Testing memoized fibonacci...")
        for n in [0, 1, 10, 15]:
            print(f"Fib({n}): {memoized_fibonacci(n)}")
        print()

        print("Testing spell dispatcher...")
        dispatcher = spell_dispatcher()
        print(dispatcher(42))
        print(dispatcher("fireball"))
        print(dispatcher([1, 2, 3]))
        print(dispatcher(3.14))
        print()

        print("Testing partial enchanter...")
        enchanters = partial_enchanter(base_enchantment)
        print(enchanters["fire"](target="Sword"))
        print(enchanters["ice"](target="Shield"))
        print(enchanters["lightning"](target="Staff"))
        print()

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
