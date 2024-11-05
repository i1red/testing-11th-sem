import pytest

from lab01.utility.parsers import parse_bool, parse_optional


def test_parse_bool():
    parser = parse_bool(truthy="yes", falsy="no")

    assert parser("yes")
    assert not parser("no")


def test_parse_bool_invalid():
    parser = parse_bool(truthy="yes", falsy="no")
    with pytest.raises(ValueError):
        parser("maybe")


def test_parse_optional():
    parser = parse_optional(null="*")

    assert parser("*") is None
    assert parser("text") == "text"
