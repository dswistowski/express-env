from functools import singledispatch

from express_env.config import EnvConfig


@singledispatch
def render(value: EnvConfig) -> str:
    raise NotImplementedError(f"render for {value.__class__.__name__} is not implemented")