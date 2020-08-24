class World:
    def __init__(self, client):
        self.client = client
        self.main_player = None
        self.other_players = []

    def show(self):
        self.main_player.show()
        for other_player in self.other_players:
            other_player.show()
        self.client.map.terrain.show()
        self.client.map.tower.show()
        self.client.map.tower2.show()
        self.client.map.background_image.show()
        self.client.camera.reparent_to(self.main_player)
