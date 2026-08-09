# typed-errs

Small, typed `Result` and `Option` values for Python code that wants explicit
failure paths without exceptions crossing API boundaries.

```bash
uv add typed-errs
```

## Example

```python
from enum import Enum, auto
from typed_errs import Err, Ok, Result, catch_bubble


class ReadError(Enum):
    NOT_FOUND = auto()


def read_name() -> Result[str, ReadError]:
    return Ok("Veya")


@catch_bubble
def greeting() -> Result[str, ReadError]:
    name = read_name().q
    return Ok(f"hello {name}")
```

Define each application's error categories as normal `Enum` classes. `Err`
stores that enum plus an optional `Diagnostic`, namespace, and context message.
The package also provides `Some`, `Nothing`, `Option`, `catch_bubble`, and
`catch_nothing`.

## Where I use it

This is my internal error-handling base for 42 projects. The generic `Result`,
`Option`, diagnostics, and bubbling helpers come from
[Pacman](https://github.com/Valentins-and-Veyas-42-group-projects/pac-man), a
work-in-progress group project in the 42 organization.
The same pattern is used throughout
[RAG Against the Machine](https://github.com/0xveya/42-rag-against-the-machine),
[call_me_maybe](https://github.com/0xveya/call_me_maybe), and
[fly-in](https://github.com/0xveya/42-fly-in) for CLI, file parsing, storage,
indexing, watcher, and web-service failures. Projects define their own error
`Enum` and return `Ok` or `Err` instead of copying the implementation again.

## Dependencies

No runtime dependencies. Python 3.10 or newer.

## Development and release

Run `mise run check` for lint, type checks, tests, and a package build. Every
push to `master` publishes a unique `0.0.<CI run>` ZeroVer version through PyPI Trusted
Publishing. `mise run publish` remains available for manual publishing.
