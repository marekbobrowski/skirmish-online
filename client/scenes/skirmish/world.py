from scenes.skirmish.zone import Zone


class World:
    def __init__(self, skirmish):
        self.skirmish = skirmish
        self.core = skirmish.core
        self.node = self.skirmish.node_3d
        self.zone = Zone(self.core, self.node, self.core.aspect2dp)

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



