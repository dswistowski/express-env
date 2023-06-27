from collections.abc import Sequence
from dataclasses import dataclass


@dataclass(frozen=True)
class Command:
    command: str
    args: Sequence[str] = ()

    def render(self):
        return " ".join([self.command, *self.args])


@dataclass(frozen=True)
class CommandSubstitution:
    command: Command


@dataclass(frozen=True)
class ConstValue:
    value: str


@dataclass(frozen=True)
class EnvironmentAssigment:
    variable: str
    value: CommandSubstitution | ConstValue
