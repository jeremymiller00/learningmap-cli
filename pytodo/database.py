"""This module provide Pytodo database functionality"""
# pytodo/database.py

import json
import configparser
from pathlib import Path
from typing import Any, Dict, List, NamedTuple

from pytodo import DB_READ_ERROR, DB_WRITE_ERROR, JSON_ERROR, SUCCESS

DEFAULT_DB_FILE_PATH = Path.home().joinpath(
    "." + Path.home().stem + "_todo.json"
)

def get_database_path(config_file: Path) -> Path:
    """Return the current path to the todo database"""
    config_parser = configparser.ConfigParser()
    config_parser.read(config_file)
    return Path(config_parser["General"]["database"])

def init_database(db_path: Path) -> int:
    """Create todo database"""
    try:
        db_path.write_text("[]") # empty todo list
        return SUCCESS
    except OSError:
        return DB_WRITE_ERROR

class DBResponse(NamedTuple):
    """
    Represents todo items returned from database
    
    A single item is:
    todo = {
        "Description": "Get some milk.",
        "Priority": 2,
        "Done": True,
    }
    """
    todo_list = List[Dict[str, any]]
    error: int

class DatabaseHandler:
    def __init__(self, db_path: Path) -> None:
        self._db_path = db_path
    
    def read_todos(self) -> DBResponse:
        try:
            with self._db_path.open("r") as db:
                try:
                    return DBResponse(json.load(db), SUCCESS)
                # catch wrong JSON format
                except json.JSONDecodeError:
                    return DBResponse([], JSON_ERROR)
        # catch file io problems
        except OSError:
            return DBResponse([], DB_READ_ERROR)

    def write_todos(self, todo_list: List[Dict[str, Any]]) -> DBResponse:
        try:
            with self._db_path.open("w") as db:
                json.dump(todo_list, db, indent=4)
            return DBResponse(todo_list, SUCCESS)
        # catch file io problems
        except OSError:
            return DBResponse(todo_list, DB_WRITE_ERROR)