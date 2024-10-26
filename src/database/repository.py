"""
This module contains a generic repository class for JSON-based data storage.
"""

import json
import os
from typing import TypeVar, Generic, Any
from datetime import datetime

T = TypeVar("T")


class JsonRepository(Generic[T]):
    """
    Generic repository class for JSON-based data storage.
    Stores each entity in a separate JSON file.
    """

    def __init__(self, directory_path: str):
        self.directory_path: str = directory_path
        self._ensure_directory_exists()

    def _ensure_directory_exists(self):
        """Ensure the directory exists"""
        os.makedirs(self.directory_path, exist_ok=True)

    def _get_file_path(self, id: str) -> str:
        """Get the file path for a specific entity"""
        return os.path.join(self.directory_path, f"{id}.json")

    def _read_file(self, file_path: str) -> dict:
        """Read data from a specific JSON file"""
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                return json.load(f)
        raise FileNotFoundError(f"File not found: {file_path}")

    def _write_file(self, file_path: str, data: dict):
        """Write data to a specific JSON file"""
        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)

    def find_all(self) -> list[dict]:
        """Retrieve all records"""
        results = []
        for filename in os.listdir(self.directory_path):
            if filename.endswith(".json"):
                file_path: str = os.path.join(self.directory_path, filename)
                data = self._read_file(file_path)
                if data:
                    results.append(data)
        if results:
            return sorted(results, key=lambda x: x.get("id"))
        return []

    def find_by_id(self, id: str) -> dict | None:
        """Find a record by ID"""
        file_path = self._get_file_path(id)
        return self._read_file(file_path)

    def find_by_field(self, field: str, value: Any) -> list[dict]:
        """Find records by field value"""
        return [item for item in self.find_all() if item.get(field) == value]

    def create(self, item: dict) -> dict:
        """Create a new record"""
        if "id" not in item:
            # Generate a timestamp-based ID for better uniqueness
            item["id"] = str(int(datetime.now().timestamp() * 1000))
        item["created_at"] = datetime.now().isoformat()

        file_path = self._get_file_path(item["id"])
        self._write_file(file_path, item)
        return item

    def update(self, id: str, item: dict) -> dict | None:
        """Update an existing record"""
        file_path: str = self._get_file_path(id=id)
        existing = self._read_file(file_path=file_path)

        if existing:
            item["id"] = id
            item["updated_at"] = datetime.now().isoformat()
            item["created_at"] = existing.get("created_at")
            self._write_file(file_path, item)
            return item
        return None

    def delete(self, id: str) -> bool:
        """Delete a record"""
        file_path = self._get_file_path(id)
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False
