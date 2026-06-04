from abc import ABC, abstractmethod
from ex0.creatures import Creature
from ex1.capabilities import HealCapability, TransformCapability


class InvalidStrategyError(Exception):
    """Raised when a strategy is used with an incompatible creature."""
    pass


class BattleStrategy(ABC):
    """Abstract base class for battle strategies."""

    @abstractmethod
    def is_valid(self, creature: Creature) -> bool:
        """Return True if creature is suitable for this strategy."""
        pass

    @abstractmethod
    def act(self, creature: Creature) -> None:
        """Execute the strategy for the creature."""
        pass


class NormalStrategy(BattleStrategy):
    """Strategy suitable for any creature."""

    def is_valid(self, creature: Creature) -> bool:
        """Any creature is valid for normal strategy."""
        return True

    def act(self, creature: Creature) -> None:
        """Simply attack."""
        print(creature.attack())


class DefensiveStrategy(BattleStrategy):
    """Strategy suitable for creatures with heal capability."""

    def is_valid(self, creature: Creature) -> bool:
        """Return True if creature has HealCapability."""
        return isinstance(creature, HealCapability)

    def act(self, creature: Creature) -> None:
        """Attack then heal."""
        if not self.is_valid(creature):
            raise InvalidStrategyError(
                f"Invalid Creature '{creature._name}' "
                f"for this defensive strategy"
            )
        assert isinstance(creature, HealCapability)
        print(creature.attack())
        print(creature.heal())


class AggressiveStrategy(BattleStrategy):
    """Strategy suitable for creatures with transform capability."""

    def is_valid(self, creature: Creature) -> bool:
        """Return True if creature has TransformCapability."""
        return isinstance(creature, TransformCapability)

    def act(self, creature: Creature) -> None:
        """Transform, attack, then revert."""
        if not self.is_valid(creature):
            raise InvalidStrategyError(
                f"Invalid Creature '{creature._name}' "
                f"for this aggressive strategy"
            )
        assert isinstance(creature, TransformCapability)
        print(creature.transform())
        print(creature.attack())
        print(creature.revert())
