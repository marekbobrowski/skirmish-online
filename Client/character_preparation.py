from direct.gui.OnscreenImage import OnscreenImage
from direct.actor.Actor import Actor
from panda3d.core import GraphicsOutput
from direct.gui.DirectGui import DirectFrame, DirectEntry, DirectButton, DirectLabel, DirectScrollBar, DGG
from direct.gui.OnscreenText import OnscreenText
from direct.particles.ParticleEffect import ParticleEffect
from panda3d.core import PointLight


class CharacterPreparation:

    def __init__(self, client):
        self.client = client
        self.client.enable_particles()
        self.client.disable_mouse()
        self.client.camera.set_pos(-2.9, -4.9, 0.94)
        self.client.camera.set_h(-50)
        self.client.world.map.terrain = self.client.loader.load_model('models/terrain.egg')
        self.client.world.map.terrain.reparent_to(self.client.render)
        self.client.world.map.tower = self.client.loader.load_model('models/tower.egg')
        self.client.world.map.tower.reparent_to(self.client.render)
        self.client.world.map.tower.set_scale(0.5)
        self.client.world.map.tower.set_pos(5, 5, 0.4)
        self.client.world.map.tower2 = self.client.loader.load_model('models/tower2.egg')
        self.client.world.map.tower2.reparent_to(self.client.render)
        self.client.world.map.tower2.set_scale(0.15)
        self.client.world.map.tower2.set_pos(-1, -3.5, 0.7)
        self.client.world.map.tower2.set_h(30)

        self.selected_class = 0

        self.knight = Actor("models/knight", {'idle': 'models/animations/knight-Idle',
                                              'run': 'models/animations/knight-Walk',
                                              'attack': 'models/animations/knight-Attack',
                                              'hit': 'models/animations/knight-Hit',
                                              'die': 'models/animations/knight-Die'})
        self.knight.reparent_to(self.client.render)
        self.knight.set_scale(0.025)
        self.knight.set_pos(-2.0, -4.1, 0.92)
        self.knight.set_h(-60)
        self.knight.loop('idle')

        # self.p = ParticleEffect()
        # self.p.loadConfig('particle_effects/test.ptf')
        # self.p.start(parent=self.knight.expose_joint(None, 'modelRoot', 'thumb_l'), renderParent=self.client.render)
        # print(self.knight.listJoints())
        # self.plight = PointLight('plight')
        # self.plight.set_max_distance(0.001)
        # self.plight.set_color((0.8, 0.1, 0.1, 1))
        # self.plnp = self.client.render.attach_new_node(self.plight)
        # self.plnp.reparent_to(self.knight.expose_joint(None, 'modelRoot', 'thumb_l'))
        # self.client.render.set_light(self.plnp)

        self.priest = Actor("models/priest", {'idle': 'models/animations/priest-Idle',
                                              'run': 'models/animations/priest-Walk',
                                              'attack': 'models/animations/priest-Attack',
                                              'hit': 'models/animations/priest-Hit',
                                              'die': 'models/animations/priest-Die'})
        self.priest.reparent_to(self.client.render)
        self.priest.set_scale(0.02)
        self.priest.set_pos(-2.0, -4.1, 0.9)
        self.priest.set_h(-60)
        self.priest.loop('idle')

        self.archer = Actor("models/archer", {'idle': 'models/animations/archer-Idle',
                                              'run': 'models/animations/archer-Walk',
                                              'attack': 'models/animations/archer-Attack',
                                              'hit': 'models/animations/archer-Hit',
                                              'die': 'models/animations/archer-Die'})
        self.archer.reparent_to(self.client.render)
        self.archer.set_scale(0.02)
        self.archer.set_pos(-1.96, -4.06, 0.9)
        self.archer.set_h(-60)
        self.archer.loop('idle')

        self.mage = Actor("models/mage", {'idle': 'models/animations/mage-Idle',
                                          'run': 'models/animations/mage-Walk',
                                          'attack': 'models/animations/mage-Attack',
                                          'hit': 'models/animations/mage-Hit',
                                          'die': 'models/animations/mage-Die'})
        self.mage.reparent_to(self.client.render)
        self.mage.set_scale(0.02)
        self.mage.set_pos(-1.80, -3.95, 0.9)
        self.mage.set_h(-60)
        self.mage.loop('idle')

        self.hide_every_character()

        self.client.world.map.background_image = OnscreenImage(parent=render2dp, image="artwork/map_background.jpg")
        self.client.world.map.background_image.set_scale(1)
        self.client.cam2dp.node().getDisplayRegion(0).setSort(-20)
        self.client.menu.hide()

        self.warrior_btn = DirectButton(scale=0.34, pos=(-1.5, 0, 0.6), frameColor=(0, 0, 0, 0),
                                        image='artwork/warrior-class.png',
                                        image_scale=0.3,
                                        rolloverSound=self.client.menu.rollover_sound,
                                        clickSound=self.client.menu.click_sound,
                                        command=self.show_warrior_only)

        self.mage_btn = DirectButton(scale=0.34, pos=(-1.5, 0, 0.3), frameColor=(0, 0, 0, 0),
                                     image='artwork/mage-class.png',
                                     image_scale=0.3,
                                     rolloverSound=self.client.menu.rollover_sound,
                                     clickSound=self.client.menu.click_sound,
                                     command=self.show_mage_only)

        self.priest_btn = DirectButton(scale=0.34, pos=(-1.5, 0, 0), frameColor=(0, 0, 0, 0),
                                       image='artwork/priest-class.png',
                                       image_scale=0.3,
                                       rolloverSound=self.client.menu.rollover_sound,
                                       clickSound=self.client.menu.click_sound,
                                       command=self.show_priest_only)

        self.archer_btn = DirectButton(scale=0.34, pos=(-1.5, 0, -0.3), frameColor=(0, 0, 0, 0),
                                       image='artwork/archer-class.png',
                                       image_scale=0.3,
                                       rolloverSound=self.client.menu.rollover_sound,
                                       clickSound=self.client.menu.click_sound,
                                       command=self.show_archer_only)

        self.class_name_text = OnscreenText(text='', font=self.client.menu.logo_font,
                                            pos=(1, 0.6), scale=0.1, mayChange=True)

        self.player_name_entry = DirectEntry(scale=0.1, pos=(-0.4, 0, -0.9), frameColor=(1, 1, 1, 0.1),
                                             entryFont=self.client.menu.logo_font,
                                             width=7, relief=DGG.RIDGE)
        self.join_world_btn = DirectButton(scale=0.34, pos=(1, 0, -0.85), frameColor=(0, 0, 0, 0),
                                           text_font=self.client.menu.logo_font,
                                           text_fg=(1, 1, 1, 0.8), text_pos=(0, -0.05), text_scale=0.18,
                                           text='Join world', image='artwork/button.png',
                                           image_scale=(1.1, 1, 0.3),
                                           rolloverSound=self.client.menu.rollover_sound,
                                           clickSound=self.client.menu.click_sound,
                                           command=self.join_game)
        self.join_world_btn.set_transparency(1)
        self.character_description_text = OnscreenText(text='',
                                                       font=self.client.menu.logo_font,
                                                       fg=(1, 1, 1, 0.8),
                                                       pos=(1, 0.15), scale=0.07, mayChange=True,
                                                       frame=(0, 0, 0, 0.8),
                                                       bg=(0, 0, 0, 0.8))
        self.show_mage_only()

    def show_warrior_description(self):
        self.class_name_text.setText('Warrior')
        self.class_name_text.setFg((1, 0, 0, 1))
        self.character_description_text.setText('Abilities: '
                                                '\n ability 1 - lorem ipsum'
                                                '\n ability 2 - lorem iisppsum'
                                                '\n ability 3 - loreeem ipsm')

    def show_mage_description(self):
        self.class_name_text.setText('Mage')
        self.class_name_text.setFg((0, 0, 1, 1))
        self.character_description_text.setText('Abilities: '
                                                '\n fireball - fajny ogieniek'
                                                '\n nova - fajny wybuch'
                                                '\n ability 3 - loreeem ipsm')

    def show_priest_description(self):
        self.class_name_text.setText('Priest')
        self.class_name_text.setFg((1, 1, 1, 1))
        self.character_description_text.setText('Abilities: '
                                                '\n ability 1 - lorem ipsum'
                                                '\n ability 2 - lorem iisppsum'
                                                '\n ability 3 - loreeem ipsm')

    def show_archer_description(self):
        self.class_name_text.setText('Archer')
        self.class_name_text.setFg((0, 0, 1, 1))
        self.character_description_text.setText('Abilities: '
                                                '\n zarombista strzala - aauu boli'
                                                '\n ability 2 - lorem iisppsum'
                                                '\n ability 3 - loreeem ipsm')

    def hide_every_gui_element(self):
        self.warrior_btn.hide()
        self.mage_btn.hide()
        self.priest_btn.hide()
        self.archer_btn.hide()
        self.player_name_entry.hide()
        self.join_world_btn.hide()
        self.class_name_text.hide()
        self.character_description_text.hide()

    def hide_scenery(self):
        self.client.world.map.terrain.hide()
        self.client.world.map.tower.hide()
        self.client.world.map.tower2.hide()
        self.client.world.map.background_image.hide()

    def hide_every_character(self):
        self.priest.hide()
        self.archer.hide()
        self.mage.hide()
        self.knight.hide()

    def show_warrior_only(self):
        self.selected_class = 0
        self.show_warrior_description()
        self.hide_every_character()
        self.knight.show()

    def show_priest_only(self):
        self.selected_class = 2
        self.show_priest_description()
        self.hide_every_character()
        self.priest.show()

    def show_mage_only(self):
        self.selected_class = 1
        self.show_mage_description()
        self.hide_every_character()
        self.mage.show()

    def show_archer_only(self):
        self.selected_class = 3
        self.show_archer_description()
        self.hide_every_character()
        self.archer.show()

    def join_game(self):
        self.hide()
        self.client.menu.display_notification('Logging in...')
        if self.client.network_manager.ask_for_pass(self.player_name_entry.get(), self.selected_class):
            self.client.menu.display_notification('Successfully logged in!\nLoading world...')
            if self.client.network_manager.ask_for_initial_data():
                self.client.network_manager.start_listening_for_updates()
                self.client.network_manager.start_sending_updates()
                self.client.menu.hide()
                self.client.world.show()
                self.client.world.enable_character_control()
            else:
                self.client.menu.display_notification('Failed to load world.')
                self.client.menu.back_to_main_btn.show()
        else:
            self.client.menu.display_notification('Failed to log in.')
            self.client.menu.back_to_main_btn.show()

    def hide(self):
        self.hide_every_gui_element()
        self.hide_every_character()
        self.hide_scenery()
