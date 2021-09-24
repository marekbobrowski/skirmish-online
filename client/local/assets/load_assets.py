from client.local.assets import asset_names as assets
from client.local import core


def load_assets_to_cache():
    for asset_2d in assets.list_2d:
        if asset_2d != "":
            core.instance.loader.load_texture(asset_2d)
    for asset_3d in assets.list_3d:
        if asset_3d != "":
            core.instance.loader.load_model(asset_3d)
    for sfx in assets.list_sfx:
        if sfx != "":
            core.instance.loader.load_sfx(sfx)
    for font in assets.list_fonts:
        if font != "":
            core.instance.loader.load_font(font)