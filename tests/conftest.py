import pytest

from express_env.plugins import ConstPlugin, OnePasswordPlugin, VaultPlugin


@pytest.fixture(
    params=[
        OnePasswordPlugin.EnvConfig(vault="foo", item="bar", field="baz"),
        VaultPlugin.EnvConfig(path="secret/foo/bar", field="baz"),
        ConstPlugin.EnvConfig("foo"),
    ],
    ids=["1password", "vault", "const"],
)
def plugin_env_config(request):
    return request.param
