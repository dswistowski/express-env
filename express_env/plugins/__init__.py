from express_env.plugins.const import ConstEnv, render_const


def init_plugins():
    from ..render import render

    render.register(ConstEnv, render_const)
