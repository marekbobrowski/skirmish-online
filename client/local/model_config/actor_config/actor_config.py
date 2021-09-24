from client.local.model_config.actor_config import dark_elf_config, dwarf_f_config
from client.local.model_config.actor_config import elf_config, kamael_config


def load(model):
    return config_mapping[model]()


def get_anim_name(model, anim):
    return anim_name_mapping[model](anim)


class Model:
    DARK_ELF = 0
    ELF = 1
    KAMAEL = 2
    DWARF_F = 3


config_mapping = {
    Model.DARK_ELF: dark_elf_config.load,
    Model.ELF: elf_config.load,
    Model.KAMAEL: kamael_config.load,
    Model.DWARF_F: dwarf_f_config.load,
}

anim_name_mapping = {
    Model.DARK_ELF: dark_elf_config.get_anim_name,
    Model.ELF: elf_config.get_anim_name,
    Model.KAMAEL: kamael_config.get_anim_name,
    Model.DWARF_F: dwarf_f_config.get_anim_name,
}
