#!usr/bin/env python3

class Plant():
    def __init__(self, name: str, height: int, age: int) -> None:
        self.name = name
        self.height = height
        self.age = age

class Flower(Plant):
    def __init__(self, name: str, height: int, age: int, color: str) -> None:
        super().__init__(name, height, age)
        self.color = color
    
    def bloom(self) -> None:
        print(f'{self.name} is blooming beautifully!')

class Tree(Plant):
    def __init__(self, name: str, height: int, age: int, trunk_diameter: int) -> None:
        super().__init__(name, height, age)
        self.trunk_diameter = trunk_diameter
    
    def produce_shade(self) -> None:
        shade = int(self.trunk_diameter * 1.56)
        print(f'{self.name} provides {shade} square meter of shade')

class Vegetable(Plant):
    def __init__(self, name: str, height: int, age: int, harvest_season: str, nutritional_value: str) -> None:
        super().__init__(name, height, age)
        self.harvest_season = harvest_season
        self.nutritional_value = nutritional_value
    
    def show_nutrition(self) -> None:
        print(f'{self.name} is rich in {self.nutritional_value}')

if __name__ == "__main__":
    print("=== Garden Plant Types ===")
    flowers = [
        Flower("Rose", 25, 30, "red"),
        Flower("Tulip", 32, 45, "yellow")
    ]
    trees = [
        Tree("Oak", 500, 1825, 50),
        Tree("Maple", 300, 500, 100)
    ]
    vegetables = [
        Vegetable("Tomato", 80, 90, "summer", "Vitamin C"),
        Vegetable("Lettuce", 15, 60, "spring", "Vitamin B")
    ]
    for flower in flowers:
        print(f"{flower.name} (Flower): {flower.height}cm, {flower.age} days, {flower.color} color")
        flower.bloom()
        print()
    for tree in trees:
        print(f"{tree.name} (Tree): {tree.height}cm, {tree.age} days, {tree.trunk_diameter}cm diameter")
        tree.produce_shade()
        print()
    for vegetable in vegetables:
        print(f"{vegetable.name} (Vegetable): {vegetable.height}cm, {vegetable.age} days, {vegetable.harvest_season} harvest")
        vegetable.show_nutrition()
        print()