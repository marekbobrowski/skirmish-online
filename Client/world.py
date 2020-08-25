from map import Map
from input_handling import InputHandling
from character_control import CharacterControl


class World:
    def __init__(self, client):
        self.client = client
        self.main_player = None
        self.other_players = []
        self.map = Map(client)
        self.input_handling = None

    def show(self):
        character_control = CharacterControl(self.main_player)
        self.input_handling = InputHandling(self.client, character_control)
        self.main_player.show()
        for other_player in self.other_players:
            other_player.show()
        self.map.terrain.show()
        self.map.tower.show()
        self.map.tower2.show()
        self.map.background_image.show()
        self.client.camera.reparent_to(self.main_player)
        self.client.camera.set_hpr(-180, -10, 0)
        self.client.camera.set_pos(0, 80, 20)
