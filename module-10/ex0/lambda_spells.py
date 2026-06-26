#!/usr/bin/env python3


def artifact_sorter(artifacts: list[dict]) -> list[dict]:
    """Sort artifacts by power level descending using lambda."""
    return sorted(artifacts, key=lambda a: a['power'], reverse=True)


def power_filter(mages: list[dict], min_power: int) -> list[dict]:
    """Filter mages with power >= min_power using lambda."""
    return list(filter(lambda m: m['power'] >= min_power, mages))


def spell_transformer(spells: list[str]) -> list[str]:
    """Add * prefix and suffix to spell names using lambda."""
    return list(map(lambda s: f"* {s} *", spells))


def mage_stats(mages: list[dict]) -> dict:
    """Calculate mage statistics using lambdas."""
    if not mages:
        return {'max_power': 0, 'min_power': 0, 'avg_power': 0.0}
    return {
        'max_power': max(mages, key=lambda m: m['power'])['power'],
        'min_power': min(mages, key=lambda m: m['power'])['power'],
        'avg_power': round(
            sum(m['power'] for m in mages) / len(mages), 2
        )
    }


def main() -> None:
    """Test all lambda functions."""
    print("Testing artifact sorter...")
    artifacts = [
        {'name': 'Crystal Orb', 'power': 85, 'type': 'orb'},
        {'name': 'Fire Staff', 'power': 92, 'type': 'staff'},
        {'name': 'Shadow Blade', 'power': 78, 'type': 'blade'},
    ]
    sorted_artifacts = artifact_sorter(artifacts)
    print(
        f"{sorted_artifacts[0]['name']}"
        f" ({sorted_artifacts[0]['power']} power)"
        f" comes before {sorted_artifacts[1]['name']}"
        f" ({sorted_artifacts[1]['power']} power)"
    )
    print()

    print("Testing spell transformer...")
    spells = ["fireball", "heal", "shield"]
    transformed = spell_transformer(spells)
    print(" ".join(transformed))
    print()

    print("Testing power filter...")
    mages = [
        {'name': 'Alex', 'power': 95, 'element': 'fire'},
        {'name': 'Jordan', 'power': 60, 'element': 'water'},
        {'name': 'Riley', 'power': 80, 'element': 'earth'},
    ]
    filtered = power_filter(mages, 75)
    for mage in filtered:
        print(f"{mage['name']}: {mage['power']} power")
    print()

    print("Testing mage stats...")
    stats = mage_stats(mages)
    print(f"Max power: {stats['max_power']}")
    print(f"Min power: {stats['min_power']}")
    print(f"Average power: {stats['avg_power']}")


if __name__ == "__main__":
    main()
