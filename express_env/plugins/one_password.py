import typing as t
from dataclasses import dataclass

from express_env import ast
from express_env.plugins.base import Plugin
from express_env.terminal import bold


@dataclass(frozen=True)
class OnePasswordEnv:
    vault: str
    item: str
    field: str


class OnePasswordPlugin(Plugin[OnePasswordEnv]):
    EnvConfig = OnePasswordEnv

    def env_config(self, data: dict[object, object]) -> OnePasswordEnv:
        match data:
            case {
                "vault": str() as vault,
                "item": str() as item,
                "field": str() as field,
            }:
                return self.EnvConfig(vault, item, field)
        raise ValueError(
            f"Invalid config for {bold('1password')} plugin, "
            f"expected {bold('vault')}, {bold('item')} and {bold('field')}: "
            f"{bold(str(data))}"
        )

    @staticmethod
    def render(config: OnePasswordEnv, key) -> t.Iterator[ast.EnvironmentAssigment]:
        yield ast.EnvironmentAssigment(
            key,
            ast.CommandSubstitution(
                ast.Command(
                    "op",
                    [
                        "item",
                        "get",
                        config.item,
                        "--vault",
                        config.vault,
                        "--field",
                        config.field,
                    ],
                )
            ),
        )
