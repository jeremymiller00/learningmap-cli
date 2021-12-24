"""This module provides the todo model-controller"""
# pytodo/pytodo.py

from pathlib import Path
from typing import Any, Dict, NamedTuple

from pytodo.database import DatabaseHandler

class CurrentTodo(NamedTuple):
    todo: Dict[str, Any]
    error: int

class Todoer:
    def __init__(self, db_path: Path) -> None:
        self._db_handler = DatabaseHandler(db_path)

