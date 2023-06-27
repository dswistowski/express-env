from express_env.plugins.base import PluginLibrary

from .const import ConstPlugin
from .vault import VaultPlugin

library = PluginLibrary()
library.register("const", ConstPlugin())
library.register("vault", VaultPlugin())


def init_plugins():
    from ..render import render

    library.register_singledispatch(render.register)
