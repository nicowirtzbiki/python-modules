#!/usr/bin/env python3

class Plant:
    def __init__(self, name: str, height: float,
                 age_days: int, growth_rate: float = 0.8) -> None:
        self.name = name
        self.height = height
        self.age_days = age_days
        self.growth_rate = growth_rate

    def grow(self) -> None:
        self.height = round(self.height + self.growth_rate, 1)

    def age(self) -> None:
        self.age_days += 1

    def show(self) -> None:
        print(f"{self.name}: {self.height}cm, {self.age_days} days old")


if __name__ == "__main__":
    rose = Plant("Rose", 25.0, 30, growth_rate=0.8)
    initial_height = rose.height

    print("=== Garden Plant Growth ===")
    for day in range(1, 8):
        print(f"=== Day {day} ===")
        rose.show()
        if day < 7:
            rose.grow()
            rose.age()

    growth = round(rose.height - initial_height, 1)
    print(f"Growth this week: {growth}cm")
