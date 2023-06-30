from collections.abc import Callable, Iterator
from typing import Any, Generic, Protocol, TypeVar

from express_env.ast import EnvironmentAssigment

EnvConfigType = TypeVar("EnvConfigType")


class Plugin(Protocol, Generic[EnvConfigType]):
    EnvConfig: type[EnvConfigType]

    def env_config(self, config: dict[object, object]) -> EnvConfigType:
        ...

    def render(self, config: EnvConfigType, key: str) -> Iterator[EnvironmentAssigment]:
        ...


class PluginLibrary:
    _plugins: dict[str, Plugin]

    def __init__(self):
        self._plugins = {}

    def register(self, name: str, plugin: Plugin[Any]) -> None:
        self._plugins[name] = plugin

    def get(self, name: str) -> Plugin:
        return self._plugins[name]

    def register_singledispatch(
        self, register: Callable[[type, Callable], None]
    ) -> None:
        for plugin in self._plugins.values():
            register(plugin.EnvConfig, plugin.render)

    @property
    def plugins_names(self) -> list[str]:
        return list(self._plugins.keys())
