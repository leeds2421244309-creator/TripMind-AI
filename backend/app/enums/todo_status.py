from enum import Enum


class TodoStatus(str, Enum):
    TODO = "todo"
    DONE = "done"