from collections.abc import Sequence
from dataclasses import dataclass
from typing import Protocol, TextIO

from express_env.config import Config


class Namespace(Protocol):
    command: str
    config: TextIO


@dataclass(frozen=True)
class Success:
    pass


@dataclass(frozen=True)
class CommandError:
    message: str


@dataclass(frozen=True)
class Context:
    config: Config
    args: Sequence[str]
