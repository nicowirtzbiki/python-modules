#!usr/bin/env python3

class SecurePlant():
    def __init__(self, name: str) -> None:
        self.name = name
        self._height = 0
        self._age = 0

    def get_height(self) -> int:
        return self._height

    def get_age(self) -> int:
        return self._age
    
    def set_height(self, height: int) -> None:
        if height < 0:
            print(f"Invalid operation attempted: height {height}cm [REJECTED]")
            print("Security: Negative height rejected")
        else:
            self._height = height
            print(f"Height updated: {height}cm [OK]")
    
    def set_age(self, age: int) -> None:
        if age < 0:
            print(f"Invalid operation attempted: age {age} days [REJECTED]")
            print("Security: Negative age rejected")
        else:
            self._age = age
            print(f"Age updated: {age} days [OK]")

if __name__ == "__main__":
    print("=== Garden Security System ===")

    plant = SecurePlant("Rose")
    print(f"Plant created: {plant.name}")

    plant.set_height(25)
    plant.set_age(30)
    print()
    plant.set_height(-5)
    print()
    print(f"Current plant: {plant.name} ({plant.get_height()}cm, {plant.get_age()} days)")