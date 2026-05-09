from .dark_validator import validate_ingredients  # circular!


def dark_spell_allowed_ingredients() -> list[str]:
    """Return allowed ingredients for dark magic."""
    return ["bats", "frogs", "arsenic", "eyeball"]


def dark_spell_record(spell_name: str, ingredients: str) -> str:
    """Record a dark spell if ingredients are valid."""
    result = validate_ingredients(ingredients)
    return f"Dark spell recorded: {spell_name} ({result})"
