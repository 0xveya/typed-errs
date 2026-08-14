# typed-errs

[![PyPI](https://img.shields.io/pypi/v/typed-errs)](https://pypi.org/project/typed-errs/)
[![CI](https://github.com/0xveya/typed-errs/actions/workflows/ci.yml/badge.svg)](https://github.com/0xveya/typed-errs/actions/workflows/ci.yml)

**[View typed-errs on PyPI](https://pypi.org/project/typed-errs/)**

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
stores that enum plus `diagnostic: Option[Diagnostic]`, a namespace, and a
context message. `Diagnostic.help_msg` is likewise an `Option[str]`, so absence
uses `Nothing()` at every layer instead of crossing through `None`. Construct
present values with `Some(Diagnostic(...))` and `Some("help text")`.

The package also provides `Some`, `Nothing`, `Option`, `catch_bubble`, and
`catch_nothing`. Result pipelines have the same `map`, `map_err`, `and_then`,
and `map_err_with` surface on both `Ok` and `Err`; error branches simply short
circuit operations that only transform successful values.

The `.q` property is intended for functions decorated with `catch_bubble`: it
unwraps `Ok` and returns the first `Err` from the decorated function. For normal
branching, use `isinstance(result, Ok)` / `isinstance(result, Err)`, `match`, or
the mapping and inspection methods. See the runnable
[pipeline example](examples/pipeline.py) for validation and early returns.

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

## Use and contributions

This is a personal library, but it is not private or locked to my projects.
You may use it in general Python work and in 42 projects under the MIT license;
just follow the rules that apply to your campus and assignment.

Contributions are welcome: open an issue or send a pull request. I do not care
whether a contribution is written by hand, AI-assisted, or generated another
way; I care about whether it is correct, tested, understandable, and a good fit.
Because this is opinionated personal infrastructure, pull requests are reviewed
selectively and are likely to be rejected unless they clearly improve the
library without making it harder to maintain.

## Development and release

Run `mise run check` for lint, type checks, tests, and a package build. Every
push to `master` publishes a unique `0.0.<CI run>` ZeroVer version through PyPI Trusted
Publishing. `mise run publish` remains available for manual publishing.
