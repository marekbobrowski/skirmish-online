from direct.actor.Actor import Actor


class BasicCharacter(Actor):
    def __init__(self, model_number, assets_dir):
        if model_number == 0:
            Actor.__init__(self, assets_dir + "models/knight", {'idle': assets_dir + 'models/animations/knight-Idle',
                                                   'run': assets_dir + 'models/animations/knight-Walk',
                                                   'attack': assets_dir + 'models/animations/knight-Attack',
                                                   'hit': assets_dir + 'models/animations/knight-Hit',
                                                   'die': assets_dir + 'models/animations/knight-Die'})
            self.set_scale(0.025)
        elif model_number == 1:
            Actor.__init__(self, assets_dir + "models/archer", {'idle': assets_dir+ 'models/animations/archer-Idle',
                                                   'run': assets_dir + 'models/animations/archer-Walk',
                                                   'attack': assets_dir + 'models/animations/archer-Attack',
                                                   'hit': assets_dir + 'models/animations/archer-Hit',
                                                   'die': assets_dir + 'models/animations/archer-Die'})
        elif model_number == 2:
            Actor.__init__(self, assets_dir + "models/mage", {'idle': assets_dir+ 'models/animations/mage-Idle',
                                                 'run': assets_dir + 'models/animations/mage-Walk',
                                                 'attack': assets_dir + 'models/animations/mage-Attack',
                                                 'hit': assets_dir + 'models/animations/mage-Hit',
                                                 'die': assets_dir + 'models/animations/mage-Die'})
            self.set_scale(0.02)
        elif model_number == 3:
            Actor.__init__(self, assets_dir + "models/priest", {'idle': assets_dir + 'models/animations/priest-Idle',
                                                   'run': assets_dir + 'models/animations/priest-Walk',
                                                   'attack': assets_dir + 'models/animations/priest-Attack',
                                                   'hit': assets_dir + 'models/animations/priest-Hit',
                                                   'die': assets_dir + 'models/animations/priest-Die'})
            self.set_scale(0.02)
