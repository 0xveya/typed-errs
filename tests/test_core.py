from enum import Enum, auto

import pytest

from typed_errs import Err, Nothing, Ok, Option, Result, Some, catch_bubble, catch_nothing


class Problem(Enum):
    BAD_INPUT = auto()


def test_result_bubbles_an_error() -> None:
    @catch_bubble
    def operation() -> Result[str, Problem]:
        value: str = Err(Problem.BAD_INPUT).q
        return Ok(value)

    assert operation() == Err(Problem.BAD_INPUT)


def test_option_bubbles_nothing() -> None:
    @catch_nothing
    def operation() -> Option[str]:
        value: str = Nothing().q
        return Some(value)

    assert operation() == Nothing()


def test_unwrap_panics_for_err() -> None:
    with pytest.raises(ValueError):
        Err(Problem.BAD_INPUT).unwrap()
