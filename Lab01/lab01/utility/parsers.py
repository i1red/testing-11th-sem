from typing import Callable


def parse_bool(*, truthy: str, falsy: str) -> Callable[[str], bool]:
    def parser(value: str) -> bool:
        if value == truthy:
            return True

        if value == falsy:
            return False

        raise ValueError

    return parser


def parse_optional(*, null: str) -> Callable[[str], str | None]:
    def parser(value: str) -> str | None:
        return value if value != null else None

    return parser
