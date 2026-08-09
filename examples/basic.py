from enum import Enum, auto

from typed_errs import Err, Ok, Result


class DivideError(Enum):
    ZERO = auto()


def divide(left: float, right: float) -> Result[float, DivideError]:
    return Err(DivideError.ZERO) if right == 0 else Ok(left / right)


print(divide(10, 2))
