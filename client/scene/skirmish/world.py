from scene.skirmish.zone import Zone
from direct.task.Task import Task

class World:
    def __init__(self, skirmish):
        self.skirmish = skirmish
        self.core = skirmish.core
        self.node = self.skirmish.node_3d
        self.zone = Zone(self.skirmish, self.node, self.core.aspect2dp)

    def load(self):
        self.zone.load()

    def spawn_player(self, player, x, y, z, h, p, r):
        player.reparent_to(self.node)
        player.set_pos_hpr(x, y, z, h, p, r)
        player.show()

    def update_player_pos_hpr(self, id_, x, y, z, h, p, r):
        player = self.skirmish.get_player_by_id(id_)
        if player is not None:
            player.set_pos_hpr(x, y, z, h, p, r)

    def update_player_z(self, task):
        x = self.skirmish.player.get_x(self.zone.terrain.get_root())
        y = self.skirmish.player.get_y(self.zone.terrain.get_root())
        elevation = self.zone.terrain.get_elevation(x, y)
        elevation_scale = self.zone.terrain.get_root().get_sz()
        self.skirmish.player.set_z(elevation * elevation_scale)
        return Task.cont



