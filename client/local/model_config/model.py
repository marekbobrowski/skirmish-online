from local.model_config import nelf_config


def load_model_config(model):
    return config_mapping[model]()


class Model:
    NIGHT_ELF = 0
    DWARF = 1
    HUMAN = 2


config_mapping = {
    Model.NIGHT_ELF: nelf_config.load
}






