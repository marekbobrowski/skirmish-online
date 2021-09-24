from client.local.assets import asset_names as assets
from client.local import core


def load():
    return core.instance.loader.load_model(assets.fiera)
