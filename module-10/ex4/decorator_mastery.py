#!/usr/bin/env python3

import time
import functools
from collections.abc import Callable
from typing import Any


def spell_timer(func: Callable) -> Callable:
    """Decorator that measures function execution time."""
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        print(f"Casting {func.__name__}...")
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"Spell completed in {elapsed:.3f} seconds")
        return result
    return wrapper


def power_validator(min_power: int) -> Callable:
    """Decorator factory that validates power levels."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            power = kwargs.get(
                'power', args[2] if len(args) > 2 else 0
            )
            if power >= min_power:
                return func(*args, **kwargs)
            return "Insufficient power for this spell"
        return wrapper
    return decorator


def retry_spell(max_attempts: int) -> Callable:
    """Decorator that retries failed spells."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    print(
                        f"Spell failed, retrying... "
                        f"(attempt {attempt}/{max_attempts})"
                    )
            return (
                f"Spell casting failed after {max_attempts} attempts"
            )
        return wrapper
    return decorator


class MageGuild:
    """Guild of mages with spell casting abilities."""

    @staticmethod
    def validate_mage_name(name: str) -> bool:
        """Validate mage name - at least 3 chars, letters and spaces."""
        return len(name) >= 3 and name.replace(" ", "").isalpha()

    @power_validator(min_power=10)
    def cast_spell(self, spell_name: str, power: int) -> str:
        """Cast a spell with power validation."""
        return f"Successfully cast {spell_name} with {power} power"


@spell_timer
def fireball() -> str:
    """Cast a fireball spell."""
    time.sleep(0.1)
    return "Fireball cast!"


@retry_spell(max_attempts=3)
def unstable_spell() -> str:
    """An unstable spell that always fails."""
    raise Exception("Spell unstable!")


@retry_spell(max_attempts=3)
def waaaaaaagh() -> str:
    """A spell that works despite the name."""
    return "Waaaaaaagh spelled !"


def main() -> None:
    """Test all decorator functions."""
    try:
        print("Testing spell timer...")
        result = fireball()
        print(f"Result: {result}")
        print()

        print("Testing retrying spell...")
        result = unstable_spell()
        print(result)
        print(waaaaaaagh())
        print()

        print("Testing MageGuild...")
        guild = MageGuild()
        print(MageGuild.validate_mage_name("Merlin"))
        print(MageGuild.validate_mage_name("X"))
        print(guild.cast_spell("Lightning", 15))
        print(guild.cast_spell("Thunder", 5))

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
