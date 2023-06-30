from io import StringIO
from unittest.mock import ANY

from express_env import ast
from express_env.config import Config, load
from express_env.plugins import ConstPlugin
from express_env.to_ast import to_ast


def test_can_load_simple_config():
    config = load(
        StringIO(
            """
env:
    FOO: bar
    BAZ:
        type: const
        value: qux
"""
        )
    )
    assert config == Config(
        env={
            "FOO": ConstPlugin.EnvConfig("bar"),
            "BAZ": ConstPlugin.EnvConfig("qux"),
        }
    )


def test_can_generate_for_plugin(plugin_env_config):
    """
    This is just smoke test to check if we can generate for plugin,
    detailed tests are in tests/plugin/test_*.py
    """
    assert list(to_ast(plugin_env_config, "FOO")) == [
        ast.EnvironmentAssigment("FOO", ANY)
    ]
