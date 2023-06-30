import argparse
import itertools
import subprocess
from collections.abc import Iterator, Sequence
from typing import Literal, TextIO

from .. import ast
from ..ast import Command
from ..config import Config
from ..to_ast import to_ast
from ..types import Namespace


class GenerateNamespace(Namespace):
    command: Literal["generate"]
    output: TextIO
    format: Literal["dotenv", "bash"]


def configure_parser(subparser: argparse._SubParsersAction):
    generate = subparser.add_parser("generate", help="generate .env file")
    generate.add_argument("--output", type=argparse.FileType("w"), default="-")
    generate.add_argument(
        "--format", type=str, choices=["dotenv", "bash"], default="dotenv"  # , "yaml"
    )


def escape_bash(value: str) -> str:
    if " " in value or '"' in value:
        escaped = value.replace("$", "\\$").replace('"', '\\"')
        return f'"{escaped}"'
    return value


def as_bash(command: Command) -> str:
    return " ".join([command.command, *map(escape_bash, command.args)])


def bash_render(lines: Sequence[ast.EnvironmentAssigment]) -> Iterator[str]:
    for assigment in lines:
        match assigment.value:
            case ast.ConstValue(value):
                yield f"{assigment.variable}={value}\n"
            case ast.CommandSubstitution(command):
                yield f"{assigment.variable}=$({as_bash(command)})\n"
    yield "\n"
    for assigment in lines:
        yield f"export {assigment.variable}\n"


def execute(command: Command) -> str:
    return (
        subprocess.check_output([command.command, *command.args])
        .decode("utf-8")
        .strip()
    )


def dotenv_renderer(lines: Sequence[ast.EnvironmentAssigment]) -> Iterator[str]:
    for assigment in lines:
        match assigment.value:
            case ast.ConstValue(value):
                yield f"{assigment.variable}={value}\n"
            case ast.CommandSubstitution(command):
                yield f"{assigment.variable}={execute(command)}\n"


def command(config: Config, namespace: GenerateNamespace, args: Sequence[str]) -> None:
    out = namespace.output
    lines = list(
        itertools.chain(*(to_ast(value, key) for key, value in config.env.items()))
    )

    if namespace.format == "dotenv":
        renderer = dotenv_renderer
    else:
        renderer = bash_render
    out.write(f"# Generated by express-env using command: \"ee {' '.join(args)}\"\n")
    for line in renderer(lines):
        out.write(line)
