def light_spell_allowed_ingredients() -> list[str]:
    """Return allowed ingredients for light magic."""
    return ["earth", "air", "fire", "water"]


def light_spell_record(spell_name: str, ingredients: str) -> str:
    """Record a light spell if ingredients are valid."""
    from alchemy.grimoire.light_validator import validate_ingredients
    result = validate_ingredients(ingredients)
    return f"Spell recorded: {spell_name} ({result})"
