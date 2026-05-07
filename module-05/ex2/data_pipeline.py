#!/usr/bin/env python3

from abc import ABC, abstractmethod
from typing import Any, Protocol


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
        """Return True if data is a string dict or list of string dicts."""
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


class ExportPlugin(Protocol):
    """Protocol defining the interface for export plugins."""

    def process_output(self, data: list[tuple[int, str]]) -> None:
        """Export a list of (rank, value) tuples."""
        ...


class CSVExport:
    """Exports data as comma-separated values."""

    def process_output(self, data: list[tuple[int, str]]) -> None:
        """Print data as a single CSV line."""
        values = [value for _, value in data]
        print("CSV Output:")
        print(",".join(values))


class JSONExport:
    """Exports data as a JSON object."""

    def process_output(self, data: list[tuple[int, str]]) -> None:
        """Print data as a JSON object with rank-based keys."""
        items = [f'"item_{rank}": "{value}"' for rank, value in data]
        print("JSON Output: " + "{" + ", ".join(items) + "}")


class DataStream:
    """Routes mixed data streams to appropriate processors."""

    def __init__(self) -> None:
        """Initialize empty list of processors."""
        self._processors: list[DataProcessor] = []

    def register_processor(self, proc: DataProcessor) -> None:
        """Register a new data processor."""
        self._processors.append(proc)

    def process_stream(self, stream: list[Any]) -> None:
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

    def output_pipeline(self, nb: int, plugin: ExportPlugin) -> None:
        """Consume nb elements from each processor and export via plugin."""
        for proc in self._processors:
            data: list[tuple[int, str]] = []
            for _ in range(min(nb, len(proc._storage))):
                data.append(proc.output())
            if data:
                plugin.process_output(data)

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
    """Test the complete data pipeline with CSV and JSON export."""
    print("=== Code Nexus - Data Pipeline ===")
    print()

    stream = DataStream()
    print("Initialize Data Stream...")
    print()
    stream.print_processors_stats()
    print()

    print("Registering Processors")
    stream.register_processor(NumericProcessor())
    stream.register_processor(TextProcessor())
    stream.register_processor(LogProcessor())
    print()

    batch1: list[Any] = [
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
    print(f"Send first batch of data on stream: {batch1}")
    print()
    stream.process_stream(batch1)
    stream.print_processors_stats()
    print()

    print("Send 3 processed data from each processor to a CSV plugin:")
    stream.output_pipeline(3, CSVExport())
    print()
    stream.print_processors_stats()
    print()

    batch2: list[Any] = [
        21,
        ["I love AI", "LLMs are wonderful", "Stay healthy"],
        [
            {"log_level": "ERROR",
             "log_message": "500 server crash"},
            {"log_level": "NOTICE",
             "log_message": "Certificate expires in 10 days"}
        ],
        [32, 42, 64, 84, 128, 168],
        "World hello"
    ]
    print(f"Send another batch of data: {batch2}")
    print()
    stream.process_stream(batch2)
    stream.print_processors_stats()
    print()

    print("Send 5 processed data from each processor to a JSON plugin:")
    stream.output_pipeline(5, JSONExport())
    print()
    stream.print_processors_stats()


if __name__ == "__main__":
    main()
