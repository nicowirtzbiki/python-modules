from abc import ABC, abstractmethod


class HealCapability(ABC):
    """Abstract class for healing capability."""

    @abstractmethod
    def heal(self) -> str:
        """Heal the creature or target."""
        pass


class TransformCapability(ABC):
    """Abstract class for transformation capability."""

    def __init__(self) -> None:
        """Initialize transform state."""
        self._transformed: bool = False

    @abstractmethod
    def transform(self) -> str:
        """Transform the creature."""
        pass

    @abstractmethod
    def revert(self) -> str:
        """Revert the creature to normal."""
        pass
