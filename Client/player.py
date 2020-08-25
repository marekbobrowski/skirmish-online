from direct.actor.Actor import Actor


class Player(Actor):
    def __init__(self, client, class_number):
        if class_number == 0:
            Actor.__init__(self, "models/knight", {'idle': 'models/animations/knight-Idle',
                                                   'run': 'models/animations/knight-Walk',
                                                   'attack': 'models/animations/knight-Attack',
                                                   'hit': 'models/animations/knight-Hit',
                                                   'die': 'models/animations/knight-Die'})
            self.set_scale(0.025)
        elif class_number == 1:
            Actor.__init__(self, "models/mage", {'idle': 'models/animations/mage-Idle',
                                                 'run': 'models/animations/mage-Walk',
                                                 'attack': 'models/animations/mage-Attack',
                                                 'hit': 'models/animations/mage-Hit',
                                                 'die': 'models/animations/mage-Die'})
            self.set_scale(0.02)
        elif class_number == 2:
            Actor.__init__(self, "models/priest", {'idle': 'models/animations/priest-Idle',
                                                   'run': 'models/animations/priest-Walk',
                                                   'attack': 'models/animations/priest-Attack',
                                                   'hit': 'models/animations/priest-Hit',
                                                   'die': 'models/animations/priest-Die'})
            self.set_scale(0.02)
        elif class_number == 3:
            Actor.__init__(self, "models/archer", {'idle': 'models/animations/archer-Idle',
                                                   'run': 'models/animations/archer-Walk',
                                                   'attack': 'models/animations/archer-Attack',
                                                   'hit': 'models/animations/archer-Hit',
                                                   'die': 'models/animations/archer-Die'})
            self.set_scale(0.02)
        self.loop('idle')
        self.client = client
        self.id = None
        self.name = 'unknown'
        self.player_class = class_number

    def set_id(self, id):
        self.id = id

    def get_id(self):
        return self.id

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def get_player_class(self):
        return self.player_class
