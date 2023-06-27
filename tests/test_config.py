from io import StringIO

from express_env.config import Config, load
from express_env.plugins import ConstPlugin


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
            "FOO": ConstPlugin.Config("bar"),
            "BAZ": ConstPlugin.Config("qux"),
        }
    )
