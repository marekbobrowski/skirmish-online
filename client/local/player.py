from direct.actor.Actor import Actor
from local import asset_names


class Player:
    def __init__(self):
        self.id = -1
        self.name = "Unknown"
        self.health = 0
        self.model = None
        self.animation = None
