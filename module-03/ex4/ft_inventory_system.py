#!/usr/bin/env python3

import sys


def parse_arguments(inventory: dict[str, int]) -> None:
    for arg in sys.argv[1:]:
        parts = arg.split(":")
        if len(parts) != 2:
            print(f"Error - invalid parameter '{arg}'")
            continue
        item, quantity = parts
        if item in inventory:
            print(f"Redundant item '{item}' - discarding")
            continue
        try:
            inventory[item] = int(quantity)
        except ValueError as e:
            print(f"Quantity error for '{item}': {e}")


def main() -> None:
    print("=== Inventory System Analysis ===")
    inventory: dict[str, int] = {}
    parse_arguments(inventory)
    print(f"Got inventory: {inventory}")
    print(f"Item list: {list(inventory.keys())}")
    total = sum(inventory.values())
    print(f"Total quantity of the {len(inventory.keys())} items: {total}")

    for item in inventory.keys():
        percentage = round(inventory[item] / total * 100, 1)
        print(f"Item {item} represents {percentage}%")

    most_abundant = list(inventory.keys())[0]
    least_abundant = list(inventory.keys())[0]

    for item in inventory.keys():
        if inventory[item] > inventory[most_abundant]:
            most_abundant = item
        if inventory[item] < inventory[least_abundant]:
            least_abundant = item

    print(f"Item most abundant: {most_abundant} "
          f"with quantity {inventory[most_abundant]}")
    print(f"Item least abundant: {least_abundant} "
          f"with quantity {inventory[least_abundant]}")

    inventory.update({"magic_item": 1})
    print(f"Updated inventory: {inventory}")


if __name__ == "__main__":
    main()
