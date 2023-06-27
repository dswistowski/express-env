import typing as t
from dataclasses import dataclass

from express_env.plugins.base import Plugin


@dataclass(frozen=True)
class VaultEnv:
    path: str
    field: str


class VaultPlugin(Plugin[VaultEnv]):
    Config = VaultEnv

    def forge(self, data: dict[object, object]) -> VaultEnv:
        match data:
            case {"path": str() as path, "field": str() as field}:
                return self.Config(path, field)
        raise ValueError(
            f"Invalid config for vault plugin, expected path and field: {data}"
        )

    @staticmethod
    def render(config: VaultEnv, key) -> t.Iterator[str]:
        yield f"{key}=$(vault read --field={config.field} {config.path})"
        yield f"export {key}"
