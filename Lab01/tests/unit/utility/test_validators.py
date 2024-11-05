from unittest.mock import Mock

import pytest

from lab01.utility.validators import optional, pipeline, validate_string, less_than, greater_than


def test_optional_with_none():
    validator = Mock()

    optional_validator = optional(validator)
    optional_validator(None)

    assert not validator.called


def test_optional_with_value():
    validator = Mock()

    optional_validator = optional(validator)
    optional_validator("abc")

    assert validator.called


def test_validate_string_valid():
    validator = validate_string(max_len=5, allowed_characters=set("abc"))
    # Should not raise any exception
    validator("abc")


def test_validate_string_too_long():
    validator = validate_string(max_len=3, allowed_characters=set("abc"))
    with pytest.raises(ValueError):
        validator("abca")


def test_validate_string_disallowed_characters():
    validator = validate_string(max_len=5, allowed_characters=set("abc"))
    with pytest.raises(ValueError):
        validator("abcd")


def test_validate_string_max_length_boundary():
    validator = validate_string(max_len=3, allowed_characters=set("abc"))
    validator("abc")
    with pytest.raises(ValueError):
        validator("abca")


def test_greater_than_valid():
    validator = greater_than(5)
    validator(5.1)


def test_greater_than_invalid():
    validator = greater_than(5)
    with pytest.raises(ValueError):
        validator(5)
    with pytest.raises(ValueError):
        validator(4)


def test_less_than_valid():
    validator = less_than(5)
    validator(4.9)


def test_less_than_invalid():
    validator = less_than(5)
    with pytest.raises(ValueError):
        validator(5)
    with pytest.raises(ValueError):
        validator(6)


def test_pipeline():
    validator = pipeline(greater_than(0), less_than(5))

    validator(0.1)
    validator(4.9)

    with pytest.raises(ValueError):
        validator(0)

    with pytest.raises(ValueError):
        validator(5)
    