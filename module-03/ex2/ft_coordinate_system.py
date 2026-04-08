import math


def get_player_pos() -> tuple[float, float, float]:
    while True:
        new_coordinates = input("Enter new coordinates "
                                "as floats in format 'x,y,z': ")
        parts = new_coordinates.split(',')
        if len(parts) != 3:
            print("Invalid syntax.")
            continue
        valid = True
        for part in parts:
            try:
                float(part.strip())
            except ValueError as e:
                print(f"Error on parameter '{part.strip()}': {e}")
                valid = False
                break
        if valid:
            return (float(parts[0].strip()),
                    float(parts[1].strip()),
                    float(parts[2].strip()))


def main() -> None:
    print("=== Game Coordinate System ===")
    print()
    print("Get a first set of coordinates:")
    first_tuple = get_player_pos()
    print(f"Got a first tuple: {first_tuple}")
    print("It includes: "
          f"X={first_tuple[0]}, Y={first_tuple[1]}, Z={first_tuple[2]}")
    distance = round(
        math.sqrt(first_tuple[0]**2 + first_tuple[1]**2 + first_tuple[2]**2),
        4
    )
    print(f"Distance to center: {distance}")
    print()
    print("Get a second set of coordinates:")
    second_tuple = get_player_pos()
    distance = round(math.sqrt(
        (second_tuple[0] - first_tuple[0])**2 +
        (second_tuple[1] - first_tuple[1])**2 +
        (second_tuple[2] - first_tuple[2])**2), 4)
    print(f"Distance between the 2 sets of coordinates: {distance}")


if __name__ == "__main__":
    main()
