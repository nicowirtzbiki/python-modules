#!/usr/bin/env python3

class Plant:
    def __init__(self, name, height, age_days):
        self.name = name
        self.height = height
        self.age_days = age_days

    def grow(self):
        self.height += 1

    def age(self):
        self.age_days += 1

    def get_info(self):
        return f"{self.name}: {self.height}cm, {self.age_days} days old"


if __name__ == "__main__":

    plants = [
        Plant("Rose", 25, 30),
        Plant("Sunflower", 80, 45),
        Plant("Cactus", 15, 120)
    ]

    print("=== Day 1 ===")
    for plant in plants:
        print(plant.get_info())

    for _ in range(6):
        for plant in plants:
            plant.grow()
            plant.age()

    print("=== Day 7 ===")
    for plant in plants:
        print(plant.get_info())
