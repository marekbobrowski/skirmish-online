from direct.task import Task


class CharacterControl:

    def __init__(self, character):
        self.character = character
        self.movement_speed = 50

    def move_forward(self, task):
        self.character.set_y(self.character, -self.movement_speed * globalClock.getDt())
        return Task.cont

    def move_backward(self, task):
        self.character.set_y(self.character, self.movement_speed * globalClock.getDt())
        return Task.cont

    def move_left(self, task):
        self.character.set_x(self.character, self.movement_speed * 0.7 * globalClock.getDt())
        return Task.cont

    def move_right(self, task):
        self.character.set_x(self.character, -self.movement_speed * 0.7 * globalClock.getDt())
        return Task.cont
