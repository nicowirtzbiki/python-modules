#!/usr/bin/env python3

class GardenError(Exception):
    def __init__(self, message: str = "Unknown garden error") -> None:
        super().__init__(message)


class PlantError(GardenError):
    def __init__(self, message: str = "Unknown plant error") -> None:
        super().__init__(message)


class WaterError(GardenError):
    def __init__(self, message: str = "Unknown water error") -> None:
        super().__init__(message)


def check_plant(plant_name: str) -> None:
    raise PlantError(f"The {plant_name} plant is wilting!")


def check_water(water_amount: int = 0) -> None:
    if water_amount == 0:
        raise WaterError(f"Not enough water in the tank!")


def test_custom_errors() -> None:
    print("=== Custom Garden Errors Demo ===")
    print()
    print("Testing PlantError...")
    try:
        check_plant("Bugonia")
    except PlantError as e:
        print(f"Caught PlantError: {e}")
    print()
    print("Testing WaterError...")
    try:
        check_water()
    except WaterError as e:
        print(f"Caught WaterError: {e}")
    print()
    print("Testing catching all garden errors...")
    try:
        check_plant("tomato")
    except GardenError as e:
        print(f"Caught GardenError: {e}")
    try:
        check_water()
    except GardenError as e:
        print(f"Caught GardenError: {e}")
    print()
    print("All custom error types work correctly!")
if __name__ == "__main__":
    test_custom_errors()