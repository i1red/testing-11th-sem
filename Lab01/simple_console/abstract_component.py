from abc import ABC, abstractmethod
from typing import Generic, TypeVar, get_args, get_origin

from simple_console.abstract_app_context import AbstractAppContext
from simple_console.run_item import RunItem

TAppContext = TypeVar("TAppContext", bound=AbstractAppContext)


class AbstractComponent(ABC, Generic[TAppContext]):
    def __init__(self, *args, **kwargs) -> None:
        try:
            context_type, = next(
                get_args(base)
                for base in self.__class__.__orig_bases__
                if get_origin(base) is AbstractComponent
            )
        except StopIteration:
            raise TypeError(
                f"{self.__class__.__name__} inherits from raw {AbstractComponent.__name__} "
                f"without generic type specified"
            )

        self._context = context_type()
        self.declare_fields(*args, **kwargs)

    @property
    def context(self) -> TAppContext:
        return self._context

    @abstractmethod
    def declare_fields(self, *args, **kwargs) -> None:
        """Declare fields"""

    @abstractmethod
    def run(self, *args, **kwargs) -> RunItem:
        """Run component"""
