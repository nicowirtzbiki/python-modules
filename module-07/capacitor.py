#!/usr/bin/env python3
from ex1 import HealingCreatureFactory, TransformCreatureFactory
from ex1.capabilities import HealCapability, TransformCapability


def test_healing(factory: HealingCreatureFactory) -> None:
    """Test healing creatures from factory."""
    print("Testing Creature with healing capability")
    for label, creature in [
        ("   base", factory.create_base()),
        ("   evolved", factory.create_evolved())
    ]:
        print(f"{label}:")
        assert isinstance(creature, HealCapability)
        print(creature.describe())
        print(creature.attack())
        print(creature.heal())
    print()


def test_transform(factory: TransformCreatureFactory) -> None:
    """Test transforming creatures from factory."""
    print("Testing Creature with transform capability")
    for label, creature in [
        ("   base", factory.create_base()),
        ("   evolved", factory.create_evolved())
    ]:
        print(f"{label}:")
        assert isinstance(creature, TransformCapability)
        print(creature.describe())
        print(creature.attack())
        print(creature.transform())
        print(creature.attack())
        print(creature.revert())
    print()


def main() -> None:
    """Run tests."""
    test_healing(HealingCreatureFactory())
    test_transform(TransformCreatureFactory())


if __name__ == "__main__":
    main()
