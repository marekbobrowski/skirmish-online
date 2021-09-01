from direct.actor.Actor import Actor


class Player:
    def __init__(self, model, id_):
        self.character = Actor.__init__(self, model)
        self.character.set_tag('id', str(id_))

        self.id = id_
        self.name = "Unknown"
        self.class_number = -1
        self.health = 0
        self.target = None
