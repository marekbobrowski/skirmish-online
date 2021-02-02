from client.scenes.character_menu.basic_character import BasicCharacter


class PlayerCharacter(BasicCharacter):
    def __init__(self, class_number, id_, name):
        BasicCharacter.__init__(self, class_number)
        self.id = id_
        self.name = name
        self.class_number = class_number

    def set_id(self, id_):
        self.id = id_

    def get_id(self):
        return self.id

    def get_class_number(self):
        return self.class_number
