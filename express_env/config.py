import typing as t
from dataclasses import dataclass

import yaml
from svarog import Svarog

from .plugins import library

EnvConfig: t.TypeAlias = t.Any | str | bool | int | float

config_forge = Svarog()


def forge_env_config(value: t.Mapping[str, str] | str | bool | int | float):
    match value:
        case bool() | int() | float() | str():
            return library.get("const").forge({"value": value})
        case {"type": str() as type_, **rest}:
            return library.get(type_).forge(rest)


@dataclass(frozen=True)
class Config:
    env: t.Mapping[str, EnvConfig]


def load(file: t.TextIO) -> Config:
    raw_config = yaml.safe_load(file)
    return Config(
        env={name: forge_env_config(value) for name, value in raw_config["env"].items()}
    )
