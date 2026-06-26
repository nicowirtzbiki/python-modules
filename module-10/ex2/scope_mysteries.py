#!/usr/bin/env python3

from collections.abc import Callable


def mage_counter() -> Callable:
    """Create a counting closure with independent state."""
    count = 0

    def counter() -> int:
        """Count calls and return current count."""
        nonlocal count
        count += 1
        return count

    return counter


def spell_accumulator(initial_power: int) -> Callable:
    """Create a power accumulator closure."""
    total = initial_power

    def accumulate(amount: int) -> int:
        """Add amount to total power and return new total."""
        nonlocal total
        total += amount
        return total

    return accumulate


def enchantment_factory(enchantment_type: str) -> Callable:
    """Create enchantment functions for different types."""
    def enchant(item_name: str) -> str:
        """Apply enchantment to item."""
        return f"{enchantment_type} {item_name}"

    return enchant


def memory_vault() -> dict[str, Callable]:
    """Create a memory management system using closures."""
    memory: dict[str, int] = {}

    def store(key: str, value: int) -> None:
        """Store a value in memory."""
        memory[key] = value

    def recall(key: str) -> int | str:
        """Recall a value from memory."""
        return memory.get(key, "Memory not found")

    return {'store': store, 'recall': recall}


def main() -> None:
    """Test all closure functions."""
    try:
        print("Testing mage counter...")
        counter_a = mage_counter()
        counter_b = mage_counter()
        print(f"counter_a call 1: {counter_a()}")
        print(f"counter_a call 2: {counter_a()}")
        print(f"counter_b call 1: {counter_b()}")
        print()

        print("Testing spell accumulator...")
        accumulator = spell_accumulator(100)
        print(f"Base 100, add 20: {accumulator(20)}")
        print(f"Base 100, add 30: {accumulator(30)}")
        print()

        print("Testing enchantment factory...")
        flaming = enchantment_factory("Flaming")
        frozen = enchantment_factory("Frozen")
        print(flaming("Sword"))
        print(frozen("Shield"))
        print()

        print("Testing memory vault...")
        vault = memory_vault()
        vault['store']('secret', 42)
        print("Store 'secret' = 42")
        print(f"Recall 'secret': {vault['recall']('secret')}")
        print(f"Recall 'unknown': {vault['recall']('unknown')}")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
