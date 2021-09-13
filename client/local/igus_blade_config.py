from . import asset_names as assets
from . import core


def load():
    return core.instance.loader.load_model(assets.igus_blade)
