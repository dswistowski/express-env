import typing as t
from dataclasses import dataclass


@dataclass(frozen=True)
class ConstEnv:
    value: str | bool | int | float
    type: t.Literal['const'] = 'const'


def render_const(value: ConstEnv) -> str:
    match value.value:
        case bool() as v:
            return 'true' if v else 'false'
        case float() as v:
            return f'%.2f'
        case int() as v:
            return f'{v}'
        case _ as v:
            return v
