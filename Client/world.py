from zone import Zone
from input_handling import InputHandling
from character_control import CharacterControl
from camera_control import CameraControl
from character import Character
from panda3d.core import Vec3


class World:
    def __init__(self, client):
        self.client = client
        self.main_player = None
        self.other_players = []
        self.zone = Zone()
        self.input_handling = None
        self.character_control = None
        self.camera_control = None
        self.camera_hook = None

    def clear_all_players(self):
        self.main_player = None
        self.other_players = []

    def show(self):
        self.main_player.show()
        for other_player in self.other_players:
            other_player.show()
        self.zone.terrain.show()
        self.zone.tower.show()
        self.zone.tower2.show()
        self.zone.background_image.show()

    def hide(self):
        self.main_player.hide()
        for other_player in self.other_players:
            other_player.hide()
        self.zone.terrain.hide()
        self.zone.tower.hide()
        self.zone.tower2.hide()
        self.zone.background_image.hide()

    def create_main_player(self, class_number, id, name, x, y, z, h, p, r):
        self.main_player = Character(self.client, class_number, id, name)
        self.main_player.reparent_to(self.client.render)
        self.main_player.set_pos_hpr(x, y, z, h, p, r)
        self.main_player.hide()
        return self.main_player

    def create_a_player(self, class_number, id, name, x, y, z, h, p, r):
        new_player = Character(self.client, class_number, id, name)
        new_player.reparent_to(self.client.render)
        new_player.set_pos_hpr(x, y, z, h, p, r)
        new_player.hide()
        self.other_players.append(new_player)
        return new_player

    def enable_character_control(self):
        self.character_control = CharacterControl(self.main_player)
        self.camera_control = CameraControl(self.client.camera)
        self.camera_control.attach_to(self.main_player, Vec3(0, 0, 5))
        self.camera_control.zoom_out()
        self.camera_control.zoom_out()
        self.camera_control.zoom_out()
        self.camera_control.zoom_out()
        self.input_handling = InputHandling(self.client, self.character_control, self.camera_control)

    def update_player_pos_hpr(self, id, x, y, z, h, p, r):
        player = self.get_player_by_id(id)
        if player is not None:
            player.set_pos_hpr(x, y, z, h, p, r)

    def get_player_by_id(self, id):
        for other_player in self.other_players:
            if other_player.id == id:
                return other_player
        return None

    def destroy_character(self, player):
        self.other_players.remove(player)
        player.delete()

