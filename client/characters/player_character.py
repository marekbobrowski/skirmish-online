from characters.basic_character import BasicCharacter


class PlayerCharacter(BasicCharacter):
    def __init__(self, class_number, id_, name, assets_dir):
        BasicCharacter.__init__(self, class_number, assets_dir)
        self.id = id_
        self.name = name
        self.class_number = class_number
        self.target = None
        self.set_tag('player_id', str(id_))

    def set_id(self, id_):
        self.id = id_

    def get_id(self):
        return self.id

    def get_class_number(self):
        return self.class_number
