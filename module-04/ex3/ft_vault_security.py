#!/usr/bin/env python3


def secure_archive(
    filename: str,
    mode: int = 0,       # 0 = ler, 1 = escrever
    content: str = ""
) -> tuple[bool, str]:
    try:
        if mode == 0:    # ler
            with open(filename, "r") as f:
                return (True, f.read())
        else:            # escrever
            with open(filename, "w") as f:
                f.write(content)
                return (True, "Content successfully written to file")
    except OSError as err:
        return (False, str(err))


def main() -> None:
    print("=== Cyber Archives Security ===")
    print()

    print("Using 'secure_archive' to read from a nonexistent file:")
    print(secure_archive("/not/existing/file"))
    print()

    print("Using 'secure_archive' to read from an inaccessible file:")
    print(secure_archive("/etc/master.passwd"))
    print()

    print("Using 'secure_archive' to read from a regular file:")
    result = secure_archive("ancient_fragment.txt")
    print(result)
    print()

    print("Using 'secure_archive' to write previous content to a new file:")
    print(secure_archive("new_fragment.txt", 1, result[1]))


if __name__ == "__main__":
    main()
