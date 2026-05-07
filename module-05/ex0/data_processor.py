#!/usr/bin/env python3

from abc import ABC, abstractmethod
from typing import Any


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
            return all(isinstance(item, (int, float)) for item in data)
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
            return all(isinstance(item, str) for item in data)
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


def main() -> None:
    """Test all data processors with valid and invalid data."""
    print("=== Code Nexus - Data Processor ===")
    print()

    print("Testing Numeric Processor...")
    num = NumericProcessor()
    print(f"Trying to validate input '42': {num.validate(42)}")
    print(f"Trying to validate input 'Hello': {num.validate('Hello')}")
    print("Test invalid ingestion of string 'foo' without prior validation:")
    try:
        num.ingest("foo")  # type: ignore
    except ValueError as e:
        print(f"Got exception: {e}")
    num.ingest([1, 2, 3, 4, 5])
    print("Processing data: [1, 2, 3, 4, 5]")
    print("Extracting 3 values...")
    for _ in range(3):
        rank, value = num.output()
        print(f"Numeric value {rank}: {value}")
    print()

    print("Testing Text Processor...")
    txt = TextProcessor()
    print(f"Trying to validate input '42': {txt.validate(42)}")
    txt.ingest(["Hello", "Nexus", "World"])
    print("Processing data: ['Hello', 'Nexus', 'World']")
    print("Extracting 1 value...")
    rank, value = txt.output()
    print(f"Text value {rank}: {value}")
    print()

    print("Testing Log Processor...")
    log = LogProcessor()
    print(f"Trying to validate input 'Hello': {log.validate('Hello')}")
    logs = [
        {"log_level": "NOTICE", "log_message": "Connection to server"},
        {"log_level": "ERROR", "log_message": "Unauthorized access!!"}
    ]
    log.ingest(logs)
    print(f"Processing data: {logs}")
    print("Extracting 2 values...")
    for _ in range(2):
        rank, value = log.output()
        print(f"Log entry {rank}: {value}")


if __name__ == "__main__":
    main()
