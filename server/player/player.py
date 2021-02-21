class Player:
    def __init__(self, connection):
        self.connection = connection
        self.joined_game = False
        self.health = 0
        self.id = 0
        self.name = 'unknown'
        self.class_number = 0
        self.x = 0
        self.y = 0
        self.z = 0
        self.h = 0
        self.p = 0
        self.r = 0

    def set_joined_game(self, joined):
        self.joined_game = joined

    def get_joined_game(self):
        return self.joined_game

    def set_id(self, id):
        self.id = id

    def get_id(self):
        return self.id

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_class_number(self, player_class):
        self.class_number = player_class

    def get_class_number(self):
        return self.class_number

    def set_pos_hpr(self, x, y, z, h, p, r):
        self.x = x
        self.y = y
        self.z = z
        self.h = h
        self.p = p
        self.r = r

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_z(self):
        return self.z

    def get_h(self):
        return self.h

    def get_p(self):
        return self.p

    def get_r(self):
        return self.r

    def get_connection(self):
        return self.connection


