from io import StringIO

from express_env.config import Config, ConstEnv, load


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
            "FOO": ConstEnv("bar"),
            "BAZ": ConstEnv("qux"),
        }
    )
