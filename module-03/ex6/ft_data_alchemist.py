#!/usr/bin/env python3

import random


def main() -> None:
    print("=== Game Data Alchemist ===")
    print()

    player_names = ["Alice", "bob", "Charlie",
                    "dylan", "Emma", "Gregory",
                    "john", "kevin", "Liam"]
    print(f"Initial list of players: {player_names}")

    player_names_capitalized = [name.capitalize() for name in player_names]
    print(f"New list with all names capitalized: {player_names_capitalized}")

    only_original_capitalized = [
        name for name in player_names if name == name.capitalize()
    ]
    print(f"New list of capitalized names only: {only_original_capitalized}")
    print()

    name_scores_dict = {
        name: random.randint(0, 999) for name in player_names_capitalized
    }
    print(f"Score dict: {name_scores_dict}")

    average_score = round(
        sum(name_scores_dict.values()) / len(name_scores_dict),
        2
    )
    print(f"Score average is {average_score}")

    highest_scores = {
        name: score
        for name, score in name_scores_dict.items()
        if score > average_score
    }
    print(f"High scores: {highest_scores}")


if __name__ == "__main__":
    main()
