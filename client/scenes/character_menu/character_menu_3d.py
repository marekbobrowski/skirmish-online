from characters.basic_character import BasicCharacter
from scenes.skirmish.zone import Zone


class CharacterMenu3D:
    def __init__(self, char_menu):
        self.char_menu = char_menu
        self.node = char_menu.node_3d
        self.class_representatives = []
        self.zone = None

    def load(self):
        self.char_menu.core.camera.set_pos(-2.9, -4.9, 0.94)
        self.char_menu.core.camera.set_h(-50)

        self.char_menu.core.world.set_zone(Zone(self.char_menu.core.loader, self.node, self.char_menu.core.render2dp))
        self.char_menu.core.cam2dp.node().getDisplayRegion(0).setSort(-20)

        knight = BasicCharacter(0)
        knight.reparent_to(self.node)
        knight.set_scale(0.025)
        knight.set_pos(-2.0, -4.1, 0.92)
        knight.set_h(-60)
        knight.loop('idle')
        self.class_representatives.append(knight)

        archer = BasicCharacter(1)
        archer.reparent_to(self.node)
        archer.set_scale(0.02)
        archer.set_pos(-1.96, -4.06, 0.9)
        archer.set_h(-60)
        archer.loop('idle')
        self.class_representatives.append(archer)

        mage = BasicCharacter(2)
        mage.reparent_to(self.node)
        mage.set_scale(0.02)
        mage.set_pos(-1.80, -3.95, 0.9)
        mage.set_h(-60)
        mage.loop('idle')
        self.class_representatives.append(mage)

        priest = BasicCharacter(3)
        priest.reparent_to(self.node)
        priest.set_scale(0.02)
        priest.set_pos(-2.0, -4.1, 0.9)
        priest.set_h(-60)
        priest.loop('idle')
        self.class_representatives.append(priest)

    def position_camera(self):
        self.char_menu.core.camera.reparent_to(self.char_menu.core.render)
        self.char_menu.core.camera.set_pos(-2.9, -4.9, 0.94)
        self.char_menu.core.camera.set_hpr(-50, 0, 0)

    def refresh(self):
        for repr_, index in self.class_representatives:
            if index != self.char_menu.selected_class:
                repr_.hide()
        self.class_representatives[self.char_menu.selected_class].show()
        self.node.show()
        self.position_camera()

    def hide(self):
        pass


