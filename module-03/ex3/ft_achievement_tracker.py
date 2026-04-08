#set(), set.union(), set.intersection(), set.difference()
import random

def gen_player_achievements() -> set[str]:
    players = ["Alice", "Bob", "Charlie", "Dylan"]
    achievements = ['Crafting Genius', 'Strategist', 
                    'World Savior', 'Speed Runner', 
                    'Survivor', 'Master Explorer', 
                    'Treasure Hunter', 'Unstoppable', 
                    'First Steps', 'Collector Supreme', 
                    ' Untouchable', 'Sharp Mind', 
                    'Boss Slayer']
    nbr_achievements = random.randint(0, len(achievements))