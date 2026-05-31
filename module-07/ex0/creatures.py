from abc import ABC, abstractmethod


class Creature(ABC):
    """Abstract base class for all creatures."""

    def __init__(self, name: str, creature_type: str) -> None:
        """Initialize creature with name and type."""
        self._name = name
        self._type = creature_type

    def describe(self) -> str:
        """Return a standard description of the creature."""
        return f"{self._name} is a {self._type} type Creature"

    @abstractmethod
    def attack(self) -> str:
        """Return attack message."""
        pass


class Flameling(Creature):
    """Fire type base creature."""

    def __init__(self) -> None:
        """Initialize Flameling."""
        super().__init__("Flameling", "Fire")

    def attack(self) -> str:
        """Return Flameling attack."""
        return f"{self._name} uses Ember!"


class Pyrodon(Creature):
    """Fire/Flying type evolved creature."""

    def __init__(self) -> None:
        """Initialize Pyrodon."""
        super().__init__("Pyrodon", "Fire/Flying")

    def attack(self) -> str:
        """Return Pyrodon attack."""
        return f"{self._name} uses Flamethrower!"


class Aquabub(Creature):
    """Water type base creature."""

    def __init__(self) -> None:
        """Initialize Aquabub."""
        super().__init__("Aquabub", "Water")

    def attack(self) -> str:
        """Return Aquabub attack."""
        return f"{self._name} uses Water Gun!"


class Torragon(Creature):
    """Water type evolved creature."""

    def __init__(self) -> None:
        """Initialize Torragon."""
        super().__init__("Torragon", "Water")

    def attack(self) -> str:
        """Return Torragon attack."""
        return f"{self._name} uses Hydro Pump!"
