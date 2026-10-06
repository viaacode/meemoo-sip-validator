from collections.abc import Iterable
from typing import Any, TypeVar, cast

T = TypeVar("T")


def collect_instances(obj: object, cls: type[T]) -> list[T]:
    """Recursively collect all instances of `cls` in a parsed descriptive model."""
    result: list[T] = []
    is_builtin = obj.__class__.__module__ == "builtins"

    if isinstance(obj, cls):
        result.append(obj)
    elif isinstance(obj, (list, tuple, set)):
        obj = cast(Iterable[Any], obj)
        for subvalue in obj:
            result += collect_instances(subvalue, cls)
    elif not is_builtin:
        for value in obj.__dict__.values():
            result += collect_instances(value, cls)

    return result
