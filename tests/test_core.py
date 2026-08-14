from enum import Enum, auto

import pytest

from typed_errs import (
    Diagnostic,
    Err,
    Nothing,
    Ok,
    Option,
    Result,
    Some,
    catch_bubble,
    catch_nothing,
)


class Problem(Enum):
    BAD_INPUT = auto()


def test_diagnostic_fields_use_options() -> None:
    diagnostic = Diagnostic("config.json", 1, "{}", 0, 1)
    error = Err(Problem.BAD_INPUT)

    assert isinstance(diagnostic.help_msg, Nothing)
    assert isinstance(error.diagnostic, Nothing)


def test_map_err_with_receives_the_complete_error() -> None:
    source = Err(
        Problem.BAD_INPUT,
        diagnostic=Some(Diagnostic("config.json", 1, "{}", 0, 1)),
    )

    mapped = source.map_err_with(lambda error: Err(Problem.BAD_INPUT, error.diagnostic))

    assert mapped.diagnostic == source.diagnostic


def test_error_short_circuits_result_pipeline() -> None:
    source = Err(Problem.BAD_INPUT)

    assert source.map(lambda value: str(value)) is source
    assert source.and_then(lambda _value: Ok("unreachable")) is source


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
