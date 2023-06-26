import argparse
from typing import TextIO, Literal

from ..config import Config
from ..render import render
from ..types import Namespace


class GenerateNamespace(Namespace):
    command: Literal["generate"]
    output: TextIO


def configure_parser(subparser: argparse._SubParsersAction):
    generate = subparser.add_parser("generate", help="generate .env file")
    generate.add_argument("output", type=argparse.FileType("w"), default="-")


def command(config: Config, namespace: GenerateNamespace):
    out = namespace.output
    for key, value in config.env.items():
        out.write(f"{key}={render(value)}\n")