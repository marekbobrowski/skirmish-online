from client.local.model_config.weapon_config import (
    igus_blade_config,
    flugel_config,
    fiera_config,
    antaras_config,
)


def load(weapon_id):
    return config_mapping[weapon_id]()


class Weapon:
    ANTARAS = 0
    FIERA = 1
    FLUGEL = 2
    IGUS_BLADE = 3


config_mapping = {
    Weapon.ANTARAS: antaras_config.load,
    Weapon.FIERA: fiera_config.load,
    Weapon.FLUGEL: flugel_config.load,
    Weapon.IGUS_BLADE: igus_blade_config.load,
}
