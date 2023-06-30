import argparse
import sys

from express_env.plugins import init_plugins
from express_env.terminal import bold
from express_env.types import CommandError, Context, Success

from .commands import all_commands
from .config import load


def main(args=sys.argv[1:]) -> bool:
    parser = argparse.ArgumentParser(
        description="Express Env CLI",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--config", type=argparse.FileType("r"), default=".ee/default.yaml"
    )
    subparser = parser.add_subparsers(
        dest="command", description="subcommands", required=True
    )
    for command in all_commands:
        command_subparser = subparser.add_parser(command.name, help=command.help)
        command.configure_subparser(command_subparser)

    namespace = parser.parse_args(args=args)

    try:
        config = load(namespace.config)
    except ValueError as e:
        print("Error while loading config: ", e.args[0])  # noqa: T201
        exit(1)
    init_plugins()

    context = Context(
        config=config,
        args=args,
    )

    for command in all_commands:
        if command.name == namespace.command:
            result = command(context, namespace)

    assert result
    match result:
        case Success():
            return True
        case CommandError(error):
            print("Error while executing command: ", bold(error))  # noqa: T201
            return False
        case _:
            raise NotImplementedError(f"Unknown result: {result}")


if __name__ == "__main__":
    if not main():
        exit(1)
