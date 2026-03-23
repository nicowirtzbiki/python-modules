#!usr/bin/env python3
class Plant():
    def __init__(self, name: str, height: int) -> None:
        self.name = name
        self.height = height
    
    def grow(self) -> None:
        self.height += 1
        print(f"{self.name} grew 1cm")

class FloweringPlant(Plant):
    def __init__(self, name: str, height: int, color: str) -> None:
        super().__init__(name, height)
        self.color = color
        self.blooming = True

class PrizeFlower(FloweringPlant):
    def __init__(self, name: str, height: int, color: str, prize_points: int) -> None:
        super().__init__(name, height, color)
        self.prize_points = prize_points

class GardenManager():

    class GardenStats:
        def __init__(self) -> None:
            self.total_growth = 0
            self.plants_added = 0

        def record_growth(self, amount: int) -> None:
            self.total_growth += amount

        def record_plant(self) -> None:
            self.plants_added += 1
        
    def __init__(self, owner: str) -> None:
        
        
if __name__ == "__main__":
    print("=== Garden Management System Demo ===")