from alchemy.elements import create_air  # absoluto
from ..potions import strength_potion    # relativo
from elements import create_fire       # relativo


def lead_to_gold() -> str:
    """Transmute lead to gold using air, strength potion and fire."""
    return (
        f"Recipe transmuting Lead to Gold: "
        f"brew '{create_air()}' and '{strength_potion()}' "
        f"mixed with '{create_fire()}'"
    )
