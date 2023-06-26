import argparse
from typing import cast

from express_env.plugins import init_plugins

from .commands import generate
from .config import load


def main(args=None):
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
    generate.configure_parser(subparser)

    namespace = parser.parse_args(args=args)
    config = load(namespace.config)
    init_plugins()

    if namespace.command == "generate":
        generate_namespace: generate.GenerateNamespace = cast(
            generate.GenerateNamespace, namespace
        )
        generate.command(config, generate_namespace)


if __name__ == "__main__":
    main()
