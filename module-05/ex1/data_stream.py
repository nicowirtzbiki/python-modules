#!/usr/bin/env python3

from abc import ABC, abstractmethod
from typing import Any
import typing


class DataProcessor(ABC):
    """Abstract base class for all data processors."""

    def __init__(self) -> None:
        """Initialize empty storage and counter."""
        self._storage: list[str] = []
        self._count: int = 0

    @abstractmethod
    def validate(self, data: Any) -> bool:
        """Check if data is valid for this processor."""
        pass

    @abstractmethod
    def ingest(self, data: Any) -> None:
        """Process and store valid data."""
        pass

    def output(self) -> tuple[int, str]:
        """Extract and return the oldest stored item with its rank."""
        rank = self._count
        data = self._storage.pop(0)
        self._count += 1
        return (rank, data)


class NumericProcessor(DataProcessor):
    """Processes numeric data: int, float, and mixed lists."""

    def validate(self, data: Any) -> bool:
        """Return True if data is int, float, or a list of both."""
        if isinstance(data, (int, float)):
            return True
        if isinstance(data, list):
            return all(isinstance(i, (int, float)) for i in data)
        return False

    def ingest(self, data: int | float | list[int | float]) -> None:
        """Convert numeric data to string and store it."""
        if not self.validate(data):
            raise ValueError("Improper numeric data")
        if isinstance(data, list):
            for item in data:
                self._storage.append(str(item))
        else:
            self._storage.append(str(data))


class TextProcessor(DataProcessor):
    """Processes text data: str and lists of str."""

    def validate(self, data: Any) -> bool:
        """Return True if data is a string or a list of strings."""
        if isinstance(data, str):
            return True
        if isinstance(data, list):
            return all(isinstance(i, str) for i in data)
        return False

    def ingest(self, data: str | list[str]) -> None:
        """Store text data as-is."""
        if not self.validate(data):
            raise ValueError("Improper text data")
        if isinstance(data, list):
            for item in data:
                self._storage.append(item)
        else:
            self._storage.append(data)


class LogProcessor(DataProcessor):
    """Processes log data: dict of strings or lists of dicts."""

    def validate(self, data: Any) -> bool:
        """Return True if data is a string dict or a list of string dicts."""
        if isinstance(data, dict):
            return all(
                isinstance(k, str) and isinstance(v, str)
                for k, v in data.items()
            )
        if isinstance(data, list):
            return all(
                isinstance(item, dict) and all(
                    isinstance(k, str) and isinstance(v, str)
                    for k, v in item.items()
                )
                for item in data
            )
        return False

    def ingest(self, data: dict[str, str] | list[dict[str, str]]) -> None:
        """Format and store log entries as 'level: message'."""
        if not self.validate(data):
            raise ValueError("Improper log data")
        if isinstance(data, list):
            for item in data:
                self._storage.append(
                    f"{item['log_level']}: {item['log_message']}"
                )
        else:
            self._storage.append(
                f"{data['log_level']}: {data['log_message']}"
            )


class DataStream:
    """Routes mixed data streams to appropriate processors."""

    def __init__(self) -> None:
        """Initialize empty list of processors."""
        self._processors: list[DataProcessor] = []

    def register_processor(self, proc: DataProcessor) -> None:
        """Register a new data processor."""
        self._processors.append(proc)

    def process_stream(self, stream: list[typing.Any]) -> None:
        """Route each element to the first processor that accepts it."""
        for element in stream:
            handled = False
            for proc in self._processors:
                if proc.validate(element):
                    proc.ingest(element)
                    handled = True
                    break
            if not handled:
                print(
                    f"DataStream error - "
                    f"Can't process element in stream: {element}"
                )

    def print_processors_stats(self) -> None:
        """Print total and remaining items for each registered processor."""
        print("== DataStream statistics ==")
        if not self._processors:
            print("No processor found, no data")
            return
        names = {
            NumericProcessor: "Numeric Processor",
            TextProcessor: "Text Processor",
            LogProcessor: "Log Processor",
        }
        for proc in self._processors:
            name = names.get(type(proc), "Unknown Processor")
            total = proc._count + len(proc._storage)
            remaining = len(proc._storage)
            print(
                f"{name}: total {total} items processed, "
                f"remaining {remaining} on processor"
            )


def main() -> None:
    """Test the DataStream with multiple processors and data batches."""
    print("=== Code Nexus - Data Stream ===")
    print()

    stream = DataStream()
    print("Initialize Data Stream...")
    stream.print_processors_stats()
    print()

    print("Registering Numeric Processor")
    stream.register_processor(NumericProcessor())
    print()

    batch: list[Any] = [
        "Hello world",
        [3.14, -1, 2.71],
        [
            {"log_level": "WARNING",
             "log_message": "Telnet access! Use ssh instead"},
            {"log_level": "INFO",
             "log_message": "User wil is connected"}
        ],
        42,
        ["Hi", "five"]
    ]

    print(f"Send first batch of data on stream: {batch}")
    stream.process_stream(batch)
    stream.print_processors_stats()
    print()

    print("Registering other data processors")
    stream.register_processor(TextProcessor())
    stream.register_processor(LogProcessor())
    print("Send the same batch again")
    stream.process_stream(batch)
    stream.print_processors_stats()
    print()

    print("Consume some elements from the data processors: "
          "Numeric 3, Text 2, Log 1")
    for _ in range(3):
        stream._processors[0].output()
    for _ in range(2):
        stream._processors[1].output()
    for _ in range(1):
        stream._processors[2].output()
    stream.print_processors_stats()


if __name__ == "__main__":
    main()
