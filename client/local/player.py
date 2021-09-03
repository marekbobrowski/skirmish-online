from direct.actor.Actor import Actor
from local import asset_names


class Player:
    def __init__(self, model, id_):
        self.character = Actor(model)
        self.character.load_anims(
            {
                'stand': asset_names.night_elf_stand,
                'run': asset_names.night_elf_run
            }
        )
        self.character.set_tag('id', str(id_))

        self.id = id_
        self.name = "Unknown"
        self.class_number = -1
        self.health = 0
        self.target = None
