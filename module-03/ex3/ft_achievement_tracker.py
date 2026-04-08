#set(), set.union(), set.intersection(), set.difference()
import random

def gen_player_achievements() -> set[str]:
    
    achievements = ['Crafting Genius', 'Strategist', 
                    'World Savior', 'Speed Runner', 
                    'Survivor', 'Master Explorer', 
                    'Treasure Hunter', 'Unstoppable', 
                    'First Steps', 'Collector Supreme', 
                    ' Untouchable', 'Sharp Mind', 
                    'Boss Slayer']
    nbr_achievements = random.randint(1, len(achievements))
    selected = random.sample(achievements, k=nbr_achievements)
    return set(selected)


def main() -> None:
    players = ["Alice", "Bob", "Charlie", "Dylan"]
    achievements = []
    for player in players:
        achievements.append(gen_player_achievements())

    print("=== Achievement Tracker System ===")
    print()
    for i in range (len(players)):
        print(f"Player {players[i]}: {achievements[i]}")
    print()
    unique_achievements = set()
    common_achievements = achievement[0]
    different_achievements = set()
    for achievement in achievements:
        unique_achievements = unique_achievements.union(achievement)
    for achievement in achievements[1:]:
        common_achievements = common_achievements.intersection(achievement)
    different_achievements = different_achievements.difference(achievement)
    print(f"All distinct achievements: {unique_achievements}")
    print()
    print(f"Common achievements: {common_achievements}")
    print()
    print()

if __name__ == "__main__":
    main()