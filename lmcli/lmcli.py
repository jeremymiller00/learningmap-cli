"""This module provides the todo controller"""
# lmcli/lmcli.py

from pathlib import Path
from typing import Any, Dict, List, NamedTuple

from lmcli import DB_READ_ERROR, ID_ERROR
from lmcli.database import DatabaseHandler

class CurrentTodo(NamedTuple):
    todo: Dict[str, Any]
    error: int

class Todoer:
    def __init__(self, db_path: Path) -> None:
        self._db_handler = DatabaseHandler(db_path)

    def add(self, description: List[str], priority: int=2) -> CurrentTodo:
        """Add a new todo to the databse"""
        description_text = " ".join(description)
        if not description_text.endswith("."):
            description_text += "."
        todo = {
            "Description": description_text,
            "Priority": priority,
            "Done": False
        }
        read = self._db_handler.read_todos()
        if read.error == DB_READ_ERROR:
            return CurrentTodo(todo, read.error)
        read.todo_list.append(todo)
        write = self._db_handler.write_todos(read.todo_list)
        return CurrentTodo(todo, write.error)
    
    def get_todo_list(self) -> List[Dict[str, Any]]:
        """Return current todo list"""
        read = self._db_handler.read_todos()
        return read.todo_list

    def set_done(self, todo_id: int) -> CurrentTodo:
        """Set todo item as done"""
        read = self._db_handler.read_todos()
        if read.error:
            return CurrentTodo({}, read.error)
        try:
            todo = read.todo_list[todo_id - 1]
        except IndexError:
            return CurrentTodo({}, ID_ERROR)
        todo["Done"] = True
        write = self._db_handler.write_todos(read.todo_list)
        return CurrentTodo(todo, write.error)
    
    def remove(self, todo_id: int) -> CurrentTodo:
        """Remove a to-do from the database using its id or index"""
        read = self._db_handler.read_todos()
        if read.error:
            return CurrentTodo({}, read.error)
        try:
            todo = read.todo_list.pop(todo_id - 1)
        except IndexError:
            return CurrentTodo({}, ID_ERROR)
        write = self._db_handler.write_todos(read.todo_list)
        return CurrentTodo(todo, write.error)
    
    def remove_all(self) -> CurrentTodo:
        """Remove all items from the todo list"""
        # overwrite the db with an empty list
        write = self._db_handler.write_todos([])
        return CurrentTodo({}, write.error)