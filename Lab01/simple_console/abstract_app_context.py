from abc import ABC
from typing import TypeVar

TAppContext = TypeVar("TAppContext")


class AbstractAppContext(ABC):
    def __new__(cls: type[TAppContext]) -> TAppContext:
        if cls is AbstractAppContext:
            raise TypeError(f"Objects of type {AbstractAppContext.__name__} cannot be instantiated.")

        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)

        return cls._instance
