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

    plant_data = [
        ("Rose", 25, 30),
        ("Oak", 200, 365),
        ("Cactus", 5, 90),
        ("Sunflower", 80, 45),
        ("Fern", 15, 120)
    ]

    plants = []

    print("=== Plant Factory Output ===")

    for name, height, age in plant_data:
        plant = Plant(name, height, age)
        plants.append(plant)
        print(
            f"Created: {plant.name} "
            f"({plant.height}cm, {plant.age_days} days)"
        )

    print(f"Total plants created: {len(plants)}")
