from dataclasses import dataclass
import typing as t

import yaml
from svarog import Svarog

from .plugins.const import ConstEnv

EnvConfig: t.TypeAlias = ConstEnv | str | bool | int | float

config_forge = Svarog()


def forge_env_config(value: t.Mapping[str, str] | str | bool | int | float):
    match value:
        case bool() | int() | float() | str():
            return config_forge.forge(ConstEnv, value)
        case {"type": "const", "value": str()}:
            return ConstEnv(value=value["value"])

    raise TypeError(f"Cannot forge {type} from {value}")


@dataclass(frozen=True)
class Config:
    env: t.Mapping[str, EnvConfig]


def load(file: t.TextIO) -> Config:
    raw_config = yaml.safe_load(file)
    return Config(
        env={
        name: forge_env_config( value)
        for name, value in raw_config["env"].items()
        }
    )