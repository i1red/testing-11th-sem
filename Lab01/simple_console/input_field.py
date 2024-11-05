from collections.abc import Callable
from dataclasses import dataclass
from typing import TypeVar, Generic, Final

from simple_console.message import display_message

PARSE_ERROR: Final[str] = "Помилка при зчитуванні даних."
VALIDATION_ERROR: Final[str] = "Введено некоректні дані."


T = TypeVar("T")


@dataclass(frozen=True, kw_only=True)
class InputField(Generic[T]):
    prompt: str
    parser: Callable[[str], T] | None = None
    validator: Callable[[T], None] = None

    def get_input(self) -> T:
        display_message(self.prompt)
        input_value = input()

        if self.parser is not None:
            try:
                input_value = self.parser(input_value)
            except Exception:
                display_message(PARSE_ERROR)
                return self.get_input()

        if self.validator is not None:
            try:
                self.validator(input_value)
            except Exception:
                display_message(VALIDATION_ERROR)
                return self.get_input()

        return input_value
