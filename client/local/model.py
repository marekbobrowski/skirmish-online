from local import dark_elf_config


def load_model_config(model):
    return config_mapping[model]()


def get_anim_name(model, anim):
    return anim_name_mapping[model](anim)


class Model:
    DARK_ELF = 0
    ELF = 1


config_mapping = {
    Model.DARK_ELF: dark_elf_config.load
}

anim_name_mapping = {
    Model.DARK_ELF: dark_elf_config.get_anim_name
}






