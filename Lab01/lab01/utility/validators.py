from collections.abc import Collection, Callable
from typing import TypeVar

T = TypeVar("T")


def optional(validator: Callable[[T], None]) -> Callable[[T | None], None]:
    def wrapper(value: T | None) -> None:
        if value is None:
            return

        validator(value)

    return wrapper


def pipeline(*validators: Callable[[T], None]) -> Callable[[T], None]:
    def wrapper(value: T) -> None:
        for validator in validators:
            validator(value)

    return wrapper


def validate_string(*, max_len: int, allowed_characters: Collection[str]) -> Callable[[str], None]:
    allowed_characters = set(allowed_characters)

    def validator(value: str) -> None:
        if len(value) > max_len:
            raise ValueError

        disallowed_characters = set(value) - allowed_characters
        if disallowed_characters:
            raise ValueError

    return validator


def greater_than(x: float, /) -> Callable[[float], None]:
    def validator(value: float) -> None:
        if value <= x:
            raise ValueError

    return validator


def less_than(x: float, /) -> Callable[[float], None]:
    def validator(value: float) -> None:
        if value >= x:
            raise ValueError

    return validator
