"""Compose fallible steps without nesting exception handlers."""

from enum import Enum, auto

from typed_errs import Err, Ok, Result, catch_bubble


class ConfigError(Enum):
    """Errors exposed by this example's configuration boundary."""

    EMPTY_PORT = auto()
    INVALID_PORT = auto()
    OUT_OF_RANGE = auto()


def parse_port(raw: str) -> Result[int, ConfigError]:
    """Parse and validate a port number."""
    if not raw:
        return Err(ConfigError.EMPTY_PORT, context_msg="PORT is empty")
    try:
        port = int(raw)
    except ValueError:
        return Err(ConfigError.INVALID_PORT, context_msg=f"Not an integer: {raw!r}")
    if not 1 <= port <= 65535:
        return Err(ConfigError.OUT_OF_RANGE, context_msg=f"Invalid TCP port: {port}")
    return Ok(port)


@catch_bubble
def server_address(host: str, raw_port: str) -> Result[str, ConfigError]:
    """Return early when parsing produces an Err."""
    port: int = parse_port(raw_port).q
    return Ok(f"http://{host}:{port}")


print(server_address("127.0.0.1", "8080"))
print(server_address("127.0.0.1", "nope"))
