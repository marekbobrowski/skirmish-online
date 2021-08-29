class Player:
    def __init__(self, connection):
        self.connection = connection
        self.joined_game = False
        self.health = 0
        self.resource = 0
        self.id = 0
        self.name = 'unknown'
        self.class_number = 0
        self.health_regen = 5
        self.resource_regen = 5
        self.cooldowns = [0, 0, 0, 0]  # cooldown left for each of 4 abilities
        self.x = 0
        self.y = 0
        self.z = 0
        self.h = 0
        self.p = 0
        self.r = 0

    def set_pos_hpr(self, x, y, z, h, p, r):
        self.x = x
        self.y = y
        self.z = z
        self.h = h
        self.p = p
        self.r = r
