#!/usr/bin/env python3

from collections.abc import Callable


def spell_combiner(spell1: Callable, spell2: Callable) -> Callable:
    """Combine two spells into one."""
    def combined(target: str, power: int) -> tuple[str, str]:
        try:
            return (spell1(target, power), spell2(target, power))
        except Exception as e:
            return (f"Spell 1 failed: {e}", f"Spell 2 failed: {e}")
    return combined


def power_amplifier(base_spell: Callable, multiplier: int) -> Callable:
    """Return a new spell with power multiplied."""
    def amplified(target: str, power: int) -> str:
        return base_spell(target, power * multiplier)
    return amplified


def conditional_caster(condition: Callable, spell: Callable) -> Callable:
    """Return a spell that only casts if condition is True."""
    def conditional(target: str, power: int) -> str:
        if condition(target, power):
            return spell(target, power)
        return "Spell fizzled"
    return conditional


def spell_sequence(spells: list[Callable]) -> Callable:
    """Return a function that casts all spells in order."""
    def sequence(target: str, power: int) -> list[str]:
        return [spell(target, power) for spell in spells]
    return sequence


def fireball(target: str, power: int) -> str:
    """Cast fireball spell."""
    return f"Fireball hits {target} for {power} damage"


def heal(target: str, power: int) -> str:
    """Cast heal spell."""
    return f"Heals {target} for {power} HP"


def shield(target: str, power: int) -> str:
    """Cast shield spell."""
    return f"Shield protects {target} with {power} defense"


def main() -> None:
    """Test all higher-order functions."""
    print("Testing spell combiner...")
    combined = spell_combiner(fireball, heal)
    result = combined("Dragon", 50)
    print(f"Combined spell result: {result[0]}, {result[1]}")
    print()

    print("Testing power amplifier...")
    mega_fireball = power_amplifier(fireball, 3)
    print(f"Original: {fireball('Dragon', 10)}")
    print(f"Amplified: {mega_fireball('Dragon', 10)}")
    print()

    print("Testing conditional caster...")
    conditional = conditional_caster(
        lambda target, power: power > 30,
        fireball
    )
    print(f"High power: {conditional('Dragon', 50)}")
    print(f"Low power: {conditional('Dragon', 10)}")
    print()

    print("Testing spell sequence...")
    sequence = spell_sequence([fireball, heal, shield])
    results = sequence("Dragon", 40)
    for r in results:
        print(f"  {r}")


if __name__ == "__main__":
    main()
