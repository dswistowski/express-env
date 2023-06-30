from collections.abc import Iterator
from functools import singledispatch

from express_env.ast import EnvironmentAssigment
from express_env.config import EnvConfig


@singledispatch
def to_ast(value: EnvConfig, name: str) -> Iterator[EnvironmentAssigment]:
    raise NotImplementedError(
        f"render for {value.__class__.__name__} is not implemented"
    )
