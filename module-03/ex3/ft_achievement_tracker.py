#!/usr/bin/env python3

import random


def gen_player_achievements() -> set[str]:
    achievements = ['Crafting Genius', 'Strategist',
                    'World Savior', 'Speed Runner',
                    'Survivor', 'Master Explorer',
                    'Treasure Hunter', 'Unstoppable',
                    'First Steps', 'Collector Supreme',
                    ' Untouchable', 'Sharp Mind',
                    'Boss Slayer', 'Hidden Path Finder']
    nbr_achievements = random.randint(1, len(achievements))
    selected = random.sample(achievements, k=nbr_achievements)
    return set(selected)


def main() -> None:
    players = ["Alice", "Bob", "Charlie", "Dylan"]
    achievements: list[set[str]] = []
    for _ in players:
        achievements.append(gen_player_achievements())

    print("=== Achievement Tracker System ===")
    print()

    for i in range(len(players)):
        print(f"Player {players[i]}: {achievements[i]}")
    print()

    unique_achievements: set[str] = set()
    for achievement in achievements:
        unique_achievements = unique_achievements.union(achievement)
    print(f"All distinct achievements: {unique_achievements}")
    print()

    common_achievements: set[str] = achievements[0]
    for achievement in achievements[1:]:
        common_achievements = common_achievements.intersection(achievement)
    print(f"Common achievements: {common_achievements}")
    print()

    for i in range(len(players)):
        others: set[str] = set()
        for j in range(len(players)):
            if i != j:
                others = others.union(achievements[j])
        print(f"Only {players[i]} has: "
              f"{achievements[i].difference(others)}")
    print()

    for i in range(len(players)):
        print(f"{players[i]} is missing: "
              f"{unique_achievements.difference(achievements[i])}")
    print()


if __name__ == "__main__":
    main()
