class SkirmishLocalUpdater:
    def __init__(self,  skirmish):
        self.skirmish = skirmish

    def update_pos_hpr(self, datagram, iterator):
        while iterator.get_remaining_size() > 0:
            id_ = iterator.get_uint8()
            x = iterator.get_float64()
            y = iterator.get_float64()
            z = iterator.get_float64()
            h = iterator.get_float64()
            p = iterator.get_float64()
            r = iterator.get_float64()
            self.skirmish.world.update_player_pos_hpr(id_, x, y, z, h, p, r)

    def update_new_player(self, datagram, iterator):
        id_ = iterator.get_uint8()
        name = iterator.get_string()
        class_number = iterator.get_uint8()
        x = iterator.get_float64()
        y = iterator.get_float64()
        z = iterator.get_float64()
        h = iterator.get_float64()
        p = iterator.get_float64()
        r = iterator.get_float64()
        self.skirmish.create_other_player(class_number, id_, name, x, y, z, h, p, r)

    def update_disconnection(self, datagram, iterator):
        id_ = iterator.get_uint8()
        self.skirmish.remove_player(id_)
