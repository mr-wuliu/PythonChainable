# PROJECT KNOWLEDGE BASE

**Generated:** 2026-04-28
**Commit:** 87bfa6a
**Branch:** main

## OVERVIEW

Python method-chaining library via two decorators (`@chainable`, `@pipeline`). Pure Python, zero runtime deps, setuptools build, Python >=3.10.

## STRUCTURE

```
pychain/
├── __init__.py      # Public API: exports `chainable`, `pipeline`
├── chainable.py     # ChainableResult proxy + @chainable decorator
├── pipeline.py      # PipelineResult proxy + @pipeline decorator
├── common.py        # CommonChain base — dunder method delegation to _value
└── enum.py          # Reserved attr name constants: _value, _instance
tests/
└── test_chainable.py  # unittest-style, 2 classes, 8 methods
```

## WHERE TO LOOK

| Task | Location | Notes |
|------|----------|-------|
| Add new chaining behavior | `pychain/chainable.py` or `pychain/pipeline.py` | Both follow identical structure |
| Add operator overloads | `pychain/common.py` | `CommonChain` base class |
| Add tests | `tests/test_chainable.py` | Inline class defs per test, unittest style |
| Modify exports | `pychain/__init__.py` | Only 2 exports currently |
| CI/CD | `.github/workflows/` | test.yml + publish.yml |

## CODE MAP

| Symbol | Type | Location | Role |
|--------|------|----------|------|
| `chainable` | decorator | `chainable.py` | Wraps return in ChainableResult proxy |
| `ChainableResult` | class | `chainable.py` | Forwards attr lookups: instance (wrap callables) → value (pass-through) |
| `pipeline` | decorator | `pipeline.py` | Wraps return in PipelineResult proxy |
| `PipelineResult` | class | `pipeline.py` | Auto-passes previous return as first arg to next method |
| `CommonChain` | class | `common.py` | Base: `__str__`, `__repr__`, `__int__`, `__float__`, `__bool__`, arithmetic, comparison — all delegate to `_value` |
| `VALUE` / `INSTANCE` | constants | `enum.py` | `"_value"`, `"_instance"` — reserved attr names |

## ARCHITECTURE

**Dependency graph**: `__init__` → `{chainable,pipeline}.py` → `common.py` → `enum.py`

**@chainable flow**: Decorated method returns value → wrapped in `ChainableResult(instance, value)` → `__getattribute__` forwards lookups to `instance` first (wrapping callables in new ChainableResult), then `value` (pass-through).

**@pipeline flow**: Same wrapping but `__getattribute__` auto-injects previous `_value` as first arg to next method call. Supports tuple unpacking for multi-return.

**CommonChain dunders**: All arithmetic (`+`, `-`, `*`, `/`, etc.) and comparison (`==`, `<`, etc.) operators delegate to `_value`. Conversion dunder (`__int__`, `__float__`, `__bool__`, `__str__`) also delegate.

## CONVENTIONS

- **PyPI name**: `pyChainable` (pip install). **Import name**: `pychain` (lowercase). Case mismatch is intentional.
- **Tests**: `unittest.TestCase` style, run via `pytest` in CI. Inline class definitions inside test methods.
- **No linter/formatter/type-checker** configured. No ruff, black, mypy, or pre-commit.
- **`requirements.txt`** is build-only (wheel, twine, build). Not used for runtime deps.
- **numpy** is test-only dependency, installed ad-hoc in CI, not declared in pyproject.toml.

## ANTI-PATTERNS (THIS PROJECT)

- **NEVER** use `_instance` or `_value` as method/property names on classes decorated with `@chainable` or `@pipeline` — these are reserved proxy state.
- **ALWAYS** use `object.__getattribute__(self, ...)` inside proxy classes (`ChainableResult`, `PipelineResult`, `CommonChain`) — normal attribute access causes infinite recursion.
- **ALWAYS** use `object.__setattr__(self, ...)` in `CommonChain.__init__` for setting `_instance`/`_value`.
- **DO NOT** rely on `type(result) is PipelineResult` or `isinstance(result, PipelineResult)` — `__class__` is proxied to return wrapped type.
- `PipelineResult.__call__` returns `self`, NOT the wrapped value — this is by design but a foot-gun.
- **Suspected bug**: `pipeline.py` line 34 returns `value` instead of `attr` for non-callable value attrs — verify before touching.

## COMMANDS

```bash
# Run tests (as CI does)
pytest --cov=pychain --cov-fail-under=50 --cov-report=term-missing -v tests/

# Run tests standalone
python tests/test_chainable.py

# Build
python -m build

# Install for development
pip install -e .
```

## NOTES

- Coverage floor is 50% — intentionally low. `common.py` and `enum.py` have only indirect test coverage.
- `test_chainable.py` manually captures `sys.stdout` via `io.StringIO` instead of pytest fixtures.
- LICENSE file still has template default author ("2018 The Python Packaging Authority").
- `pipeline.py:34` — `return value` may be a bug (should be `return attr`); matches `ChainableResult` which correctly returns `attr`.
