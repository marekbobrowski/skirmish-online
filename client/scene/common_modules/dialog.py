from direct.gui.DirectGui import DirectFrame, DirectLabel, DirectButton, DGG
import assets_dir_config


class Dialog:
    def __init__(self, core, parent, frame_size):
        self.node = parent.attach_new_node("dialog node")
        self.node.set_pos(0, 0, 0.25)
        self.core = core
        assets_dir = assets_dir_config.assets_dir
        rollover_sound = self.core.loader.loadSfx(assets_dir + 'sounds/mouse_rollover.wav')
        click_sound = self.core.loader.loadSfx(assets_dir + 'sounds/mouse_click.wav')
        font = self.core.loader.load_font(assets_dir + 'fonts/GODOFWAR.TTF')
        self.frame = DirectFrame(parent=self.node,
                                 frameSize=frame_size,
                                 frameColor=(0, 0, 0, 0.65),
                                 relief=DGG.RAISED,
                                 borderWidth=(-0.05, 0.1))

        self.label = DirectLabel(parent=self.node,
                                 text_scale=0.1,
                                 frameColor=(0, 0, 0, 0),
                                 text_fg=(1, 1, 1, 1),
                                 text='')
        self.button = DirectButton(scale=0.25,
                                   pos=(0, 0, -0.15),
                                   frameColor=(0, 0, 0, 0),
                                   text_font=font,
                                   text_fg=(1, 1, 1, 0.8),
                                   text_pos=(0, -0.05),
                                   text_scale=0.18,
                                   text='',
                                   image=assets_dir+'artwork/button.png',
                                   image_scale=(1.1, 1, 0.3),
                                   rolloverSound=rollover_sound,
                                   clickSound=click_sound,
                                   parent=self.node)
        self.button.set_transparency(1)

    def set_button(self, text, function):
        self.button['text'] = text
        self.button['command'] = function

    def set_label(self, text):
        self.label['text'] = text

    def show(self):
        self.node.show()

    def hide(self):
        self.node.hide()



