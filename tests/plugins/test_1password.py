from express_env import ast
from express_env.plugins import OnePasswordPlugin


def test_can_load_own_config():
    plugin = OnePasswordPlugin()

    assert plugin.env_config(
        {"vault": "vault", "item": "item", "field": "field"}
    ) == OnePasswordPlugin.EnvConfig("vault", "item", "field")


def test_generate_error_if_one_of_required_fields_is_missing():
    required_fields = ["vault", "item", "field"]
    plugin = OnePasswordPlugin()

    full_config = {"vault": "vault", "item": "item", "field": "field"}

    for field in required_fields:
        config = full_config.copy()
        del config[field]
        try:
            plugin.env_config(config)
        except ValueError as e:
            assert "Invalid config" in str(e)
        else:
            raise AssertionError("Should raise ValueError")


def test_can_render_command_substitution():
    plugin = OnePasswordPlugin()

    assert list(
        plugin.render(OnePasswordPlugin.EnvConfig("vault", "item", "field"), "key")
    ) == [
        ast.EnvironmentAssigment(
            "key",
            ast.CommandSubstitution(
                ast.Command(
                    "op",
                    [
                        "item",
                        "get",
                        "item",
                        "--vault",
                        "vault",
                        "--field",
                        "field",
                    ],
                )
            ),
        )
    ]
