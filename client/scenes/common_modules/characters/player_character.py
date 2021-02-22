from scenes.common_modules.characters.basic_character import BasicCharacter
from scenes.common_modules.player_classes import archer, priest, mage, warrior


class PlayerCharacter(BasicCharacter):
    def __init__(self, class_number, id_, name, health):
        BasicCharacter.__init__(self, class_number)
        self.id = id_
        self.name = name
        self.player_class = None
        if class_number == 0:
            self.player_class = warrior.Warrior
        elif class_number == 1:
            self.player_class = archer.Archer
        elif class_number == 2:
            self.player_class = mage.Mage
        elif class_number == 3:
            self.player_class = priest.Priest
        self.class_number = class_number
        self.health = health
        self.target = None
        self.set_tag('player_id', str(id_))

    def set_id(self, id_):
        self.id = id_

    def get_id(self):
        return self.id

    def get_class_number(self):
        return self.class_number

    def set_health(self, health):
        self.health = health
