import argparse
from typing import Protocol

from express_env.types import CommandError, Context, Namespace, Success


class CliCommand(Protocol):
    name: str
    help: str

    def configure_subparser(self, subparser: argparse.ArgumentParser):
        ...

    def __call__(
        self, context: Context, namespace: Namespace
    ) -> Success | CommandError:
        ...
