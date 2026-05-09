from .dark_spellbook import dark_spell_allowed_ingredients  # circular!


def validate_ingredients(ingredients: str) -> str:
    """Validate if ingredients contain at least one dark ingredient."""
    allowed = dark_spell_allowed_ingredients()
    for ingredient in allowed:
        if ingredient.lower() in ingredients.lower():
            return f"{ingredients} - VALID"
    return f"{ingredients} - INVALID"
