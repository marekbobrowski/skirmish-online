from direct.actor.Actor import Actor
import config


class PlayerCharacter(Actor):
    def __init__(self, model, id_):
        Actor.__init__(self, model)
        self.load_anims({
            'run': config.animations_dir + 'run',
            'idle': config.animations_dir + 'idle_1',
            'attack': config.animations_dir + 'attack2',
            'strafe_left': config.animations_dir + 'strafe_left',
            'strafe_right': config.animations_dir + 'strafe_right'
        })
        self.id = id_
        self.set_tag('id', str(id_))
        self.name = "Unknown"
        self.class_number = -1
        self.health = 0
        self.target = None
