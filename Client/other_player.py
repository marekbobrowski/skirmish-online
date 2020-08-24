from direct.actor.Actor import Actor


class OtherPlayer(Actor):
    def __init__(self, client, class_number):
        if class_number == 0:
            pass
        elif class_number == 1:
            pass
        elif class_number == 2:
            pass
        elif class_number == 3:
            pass
            Actor.__init__(self, "models/panda-model", {'walk': 'models/panda-walk4'})
        else:
            Actor.__init__(self, "models/panda-model", {'walk': 'models/panda-walk4'})
        self.client = client
        self.id = None
        self.name = None
        self.player_class = None

    def set_id(self, id):
        self.id = id

    def get_id(self):
        return self.id

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_player_class(self, player_class):
        self.player_class = player_class

    def get_player_class(self):
        return self.player_class
