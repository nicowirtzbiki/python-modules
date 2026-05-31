#!/usr/bin/env python3
from ex0 import FlameFactory, AquaFactory
from ex0.factories import CreatureFactory


def test_factory(factory: CreatureFactory) -> None:
    """Test that a factory can create and use both creatures."""
    print("Testing factory")
    base = factory.create_base()
    evolved = factory.create_evolved()
    print(base.describe())
    print(base.attack())
    print(evolved.describe())
    print(evolved.attack())
    print()


def test_battle(
    factory1: CreatureFactory,
    factory2: CreatureFactory
) -> None:
    """Make base creatures from two factories fight."""
    print("Testing battle")
    c1 = factory1.create_base()
    c2 = factory2.create_base()
    print(c1.describe())
    print("  vs. ")
    print(c2.describe())
    print("  fight! ")
    print(c1.attack())
    print(c2.attack())


def main() -> None:
    """Run tests."""
    flame = FlameFactory()
    aqua = AquaFactory()
    test_factory(flame)
    test_factory(aqua)
    test_battle(flame, aqua)


if __name__ == "__main__":
    main()
