from ex0.creatures import Creature
from ex0.factories import CreatureFactory
from ex1.capabilities import HealCapability, TransformCapability


class Sproutling(Creature, HealCapability):
    """Grass type base creature with healing capability."""

    def __init__(self) -> None:
        """Initialize Sproutling."""
        Creature.__init__(self, "Sproutling", "Grass")

    def attack(self) -> str:
        """Return Sproutling attack."""
        return f"{self._name} uses Vine Whip!"

    def heal(self) -> str:
        """Return Sproutling heal."""
        return f"{self._name} heals itself for a small amount"


class Bloomelle(Creature, HealCapability):
    """Grass/Fairy type evolved creature with healing capability."""

    def __init__(self) -> None:
        """Initialize Bloomelle."""
        Creature.__init__(self, "Bloomelle", "Grass/Fairy")

    def attack(self) -> str:
        """Return Bloomelle attack."""
        return f"{self._name} uses Petal Dance!"

    def heal(self) -> str:
        """Return Bloomelle heal."""
        return f"{self._name} heals itself and others for a large amount"


class Shiftling(Creature, TransformCapability):
    """Normal type base creature with transform capability."""

    def __init__(self) -> None:
        """Initialize Shiftling."""
        Creature.__init__(self, "Shiftling", "Normal")
        TransformCapability.__init__(self)

    def attack(self) -> str:
        """Return Shiftling attack based on transform state."""
        if self._transformed:
            return f"{self._name} performs a boosted strike!"
        return f"{self._name} attacks normally."

    def transform(self) -> str:
        """Transform Shiftling."""
        self._transformed = True
        return f"{self._name} shifts into a sharper form!"

    def revert(self) -> str:
        """Revert Shiftling to normal."""
        self._transformed = False
        return f"{self._name} returns to normal."


class Morphagon(Creature, TransformCapability):
    """Normal/Dragon type evolved creature with transform capability."""

    def __init__(self) -> None:
        """Initialize Morphagon."""
        Creature.__init__(self, "Morphagon", "Normal/Dragon")
        TransformCapability.__init__(self)

    def attack(self) -> str:
        """Return Morphagon attack based on transform state."""
        if self._transformed:
            return f"{self._name} unleashes a devastating morph strike!"
        return f"{self._name} attacks normally."

    def transform(self) -> str:
        """Transform Morphagon."""
        self._transformed = True
        return f"{self._name} morphs into a dragonic battle form!"

    def revert(self) -> str:
        """Revert Morphagon to normal."""
        self._transformed = False
        return f"{self._name} stabilizes its form."


class HealingCreatureFactory(CreatureFactory):
    """Factory for healing creatures."""

    def create_base(self) -> Creature:
        """Create Sproutling."""
        return Sproutling()

    def create_evolved(self) -> Creature:
        """Create Bloomelle."""
        return Bloomelle()


class TransformCreatureFactory(CreatureFactory):
    """Factory for transforming creatures."""

    def create_base(self) -> Creature:
        """Create Shiftling."""
        return Shiftling()

    def create_evolved(self) -> Creature:
        """Create Morphagon."""
        return Morphagon()
