from abc import ABC, abstractmethod
from ex0.creatures import Creature, Flameling, Pyrodon, Aquabub, Torragon


class CreatureFactory(ABC):
    """Abstract factory for creating creature families."""

    @abstractmethod
    def create_base(self) -> Creature:
        """Create base creature."""
        pass

    @abstractmethod
    def create_evolved(self) -> Creature:
        """Create evolved creature."""
        pass


class FlameFactory(CreatureFactory):
    """Factory for fire type creatures."""

    def create_base(self) -> Creature:
        """Create Flameling."""
        return Flameling()

    def create_evolved(self) -> Creature:
        """Create Pyrodon."""
        return Pyrodon()


class AquaFactory(CreatureFactory):
    """Factory for water type creatures."""

    def create_base(self) -> Creature:
        """Create Aquabub."""
        return Aquabub()

    def create_evolved(self) -> Creature:
        """Create Torragon."""
        return Torragon()
