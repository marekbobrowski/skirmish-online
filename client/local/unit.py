from direct.actor.Actor import Actor


class Unit:
    def __init__(self):
        self.id = -1
        self.name = "Unknown"
        self.health = 0
        self.model = None
        self.animation = None
        self.weapon = None
        self.base_node = None
        self.weapon_node = None
        self.actor = None
