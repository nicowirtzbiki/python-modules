#!/usr/bin/env python3

import random
from typing import Generator


def gen_events() -> Generator[tuple[str, str], None, None]:
    players = ["alice", "bob", "charlie", "dylan"]
    actions = ["run", "eat", "sleep",
               "grab", "move", "climb",
               "swim", "use", "release"]
    while True:
        yield (random.choice(players), random.choice(actions))


def consume_event(
        events: list[tuple[str, str]]
) -> Generator[tuple[str, str], None, None]:
    while len(events) > 0:
        event = random.choice(events)
        events.remove(event)
        yield event


def main() -> None:
    print("=== Game Data Stream ===")

    gen = gen_events()
    for i in range(1000):
        name, action = next(gen)
        print(f"Event {i}: Player {name} did action {action}")

    events = []
    for _ in range(10):
        events.append(next(gen))
    print(f"Built list of 10 events: {events}")

    for event in consume_event(events):
        print(f"Got event from list: {event}")
        print(f"Remains in list: {events}")


if __name__ == "__main__":
    main()
