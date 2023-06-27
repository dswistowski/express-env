import argparse
import itertools
import subprocess
from collections.abc import Iterator, Sequence
from typing import Literal, TextIO

from .. import ast
from ..ast import Command
from ..config import Config
from ..render import render
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


def bash_render(lines: Sequence[ast.EnvironmentAssigment]) -> Iterator[str]:
    for assigment in lines:
        match assigment.value:
            case ast.ConstValue(value):
                yield f"{assigment.variable}={value}\n"
            case ast.CommandSubstitution(command):
                yield f"{assigment.variable}=$({command.render()})\n"
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


def command(config: Config, namespace: GenerateNamespace):
    out = namespace.output
    lines = list(
        itertools.chain(*(render(value, key) for key, value in config.env.items()))
    )

    if namespace.format == "dotenv":
        renderer = dotenv_renderer
    else:
        renderer = bash_render
    for line in renderer(lines):
        out.write(line)
