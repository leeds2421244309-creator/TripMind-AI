from enum import Enum


class TodoSource(str, Enum):
    AI = "ai"
    USER = "user"