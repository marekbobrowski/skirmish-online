from scenes.skirmish.input_handling import InputHandling
from scenes.skirmish.character_control import CharacterControl
from scenes.skirmish.camera_control import CameraControl
from scenes.skirmish.interface import Interface
from scenes.skirmish.world import World
from characters.player_character import PlayerCharacter
from panda3d.core import Vec3
from direct.task.Task import Task


class Skirmish:
    def __init__(self, scene_manager):
        self.scene_manager = scene_manager
        self.core = scene_manager.core

        self.node_2d = self.core.aspect2d.attach_new_node("skirmish 2d node")
        self.node_3d = self.core.render.attach_new_node("skirmish 3d node")

        self.player = None
        self.other_players = []
        self.world = World(self)
        self.interface = Interface(self)
        self.character_control = None
        self.camera_control = None
        self.input_handling = None
        self._is_loaded = False

    def is_loaded(self):
        return self._is_loaded

    def load(self):
        self.node_2d.hide()
        self.node_3d.hide()

        self.world.load()
        self.interface.load()

        data_iterator, datagram = self.core.network_manager.ask_for_initial_data()
        if data_iterator is not None and datagram is not None:
            id_ = data_iterator.get_uint8()
            name = data_iterator.get_string()
            class_number = data_iterator.get_uint8()
            x = data_iterator.get_float64()
            y = data_iterator.get_float64()
            z = data_iterator.get_float64()
            h = data_iterator.get_float64()
            p = data_iterator.get_float64()
            r = data_iterator.get_float64()
            self.player = self.create_player(class_number, id_, name, x, y, z, h, p, r)

            while data_iterator.get_remaining_size() > 0:
                id_ = data_iterator.get_uint8()
                name = data_iterator.get_string()
                class_number = data_iterator.get_uint8()
                x = data_iterator.get_float64()
                y = data_iterator.get_float64()
                z = data_iterator.get_float64()
                h = data_iterator.get_float64()
                p = data_iterator.get_float64()
                r = data_iterator.get_float64()
                self.other_players.append(self.create_player(class_number, id_, name, x, y, z, h, p, r))

            # self.core.network_manager.send_ready_for_updates()
            # self.core.network_manager.start_listening_for_updates()
            # self.core.network_manager.start_sending_updates()
        else:
            self.scene_manager.show_dialog('Lost connection.')

        self._is_loaded = True

    def enter(self):
        self.node_2d.show()
        self.node_3d.show()
        self.core.task_mgr.add(self.update, "game update")
        self.enable_control()

    def leave(self):
        self.node_2d.leave()
        self.node_3d.leave()
        self.disable_control()

    def create_player(self, class_number, id_, name, x, y, z, h, p, r):
        player = PlayerCharacter(class_number, id_, name, self.core.assets_dir)
        self.world.spawn_player(player, x, y, z, h, p, r)
        return player

    def enable_control(self):
        self.character_control = CharacterControl(self.player)
        self.camera_control = CameraControl(self.core.camera)
        self.camera_control.attach_to(self.player, Vec3(0, 0, 5))
        self.camera_control.zoom_out()
        self.camera_control.zoom_out()
        self.camera_control.zoom_out()
        self.camera_control.zoom_out()
        self.input_handling = InputHandling(self)

    def disable_control(self):
        pass

    def get_player_by_id(self, id_):
        for other_player in self.other_players:
            if other_player.id == id_:
                return other_player
        return None

    def destroy_character(self, player):
        self.other_players.remove(player)
        player.delete()

    def update(self, task):
        return Task.cont
