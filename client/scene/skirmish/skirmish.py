from scenes.skirmish.input_handling import InputHandling
from scenes.skirmish.character_control import CharacterControl
from scenes.skirmish.camera_control import CameraControl
from scenes.skirmish.interface.interface import Interface
from scenes.skirmish.world import World
from scenes.skirmish.abilities import Abilities
from scenes.skirmish.object_picking import ObjectPicking
from scenes.common_modules.characters.player_character import PlayerCharacter
from panda3d.core import Vec3
import config
import core


class Skirmish:
    def __init__(self, scene_manager):
        self.scene_manager = scene_manager

        self.node_2d = core.instance.aspect2d.attach_new_node("skirmish 2d node")
        self.node_3d = core.instance.render.attach_new_node("skirmish 3d node")

        self.player = None
        self.abilities = Abilities(self)
        self.other_players = []
        self.world = World(self)
        self.interface = Interface(self)
        self.character_control = None
        self.camera_control = None
        self.input_handling = None
        self.object_picking = None
        self._is_loaded = False

    def is_loaded(self):
        return self._is_loaded

    def load(self):
        self.node_2d.hide()
        self.node_3d.hide()

        self.world.load()

        data_iterator, datagram = self.core.networking_manager.ask_for_initial_data()
        if data_iterator is not None and datagram is not None:
            id_ = data_iterator.get_uint8()
            name = data_iterator.get_string()
            class_number = data_iterator.get_uint8()
            health = data_iterator.get_uint8()
            x = data_iterator.get_float64()
            y = data_iterator.get_float64()
            z = data_iterator.get_float64()
            h = data_iterator.get_float64()
            p = data_iterator.get_float64()
            r = data_iterator.get_float64()
            self.create_main_player(id_, class_number, name, health, x, y, z, h, p, r)
            self.player.health = health
            while data_iterator.get_remaining_size() > 0:
                id_ = data_iterator.get_uint8()
                name = data_iterator.get_string()
                class_number = data_iterator.get_uint8()
                health = data_iterator.get_uint8()
                x = data_iterator.get_float64()
                y = data_iterator.get_float64()
                z = data_iterator.get_float64()
                h = data_iterator.get_float64()
                p = data_iterator.get_float64()
                r = data_iterator.get_float64()
                self.create_other_player(id_, class_number, name, health, x, y, z, h, p, r)

            self.interface.load()
        else:
            self.scene_manager.show_dialog('Lost connection.')

        self._is_loaded = True

    def enter(self):
        self.core.networking_manager.send_ready_for_updates()
        self.core.networking_manager.start_updating_skirmish(self)
        self.core.task_mgr.add(self.interface.update, "interface update")
        # self.core.task_mgr.add(self.world.update_player_z, "update main player z")
        self.node_2d.show()
        self.node_3d.show()
        self.object_picking = ObjectPicking(self)
        self.enable_control()

    def leave(self):
        self.node_2d.hide()
        self.node_3d.hide()

    def create_main_player(self, id_, class_number, name, health, x, y, z, h, p, r):
        player = PlayerCharacter(config.heroes[class_number], id_)
        player.class_number = class_number
        player.name = name
        player.health = health
        self.world.spawn_player(player, x, y, z, h, p, r)
        self.player = player
        self.player.loop('idle')

    def create_other_player(self, id_, class_number, name, health, x, y, z, h, p, r):
        player = PlayerCharacter(config.heroes[class_number], id_)
        player.class_number = class_number
        player.name = name
        player.health = health
        self.world.spawn_player(player, x, y, z, h, p, r)
        self.other_players.append(player)
        player.loop('idle')

    def enable_control(self):
        self.character_control = CharacterControl(self.player, self.core)
        self.camera_control = CameraControl(self.core.camera)
        self.camera_control.attach_to(self.player, Vec3(0, 0, 2))
        self.camera_control.zoom_out(4)
        self.input_handling = InputHandling(self)

    def get_player_by_id(self, id_):
        for other_player in self.other_players:
            if other_player.id == id_:
                return other_player
        return None

    def remove_player(self, id_):
        player = self.get_player_by_id(id_)
        if player is not None:
            self.other_players.remove(player)
            player.delete()

    def flush(self):
        for child in self.node_3d.get_children():
            child.remove_node()
        self.input_handling.disable()
        self.other_players = []
        self.player = None
        self.camera_control = None
        self.character_control = None
        self.object_picking = None
        self._is_loaded = False
        self.core.task_mgr.remove('interface update')

