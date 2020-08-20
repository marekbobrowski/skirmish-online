class CharacterPreparation:
    def __init__(self, client):
        self.client = client
        self.client.map.terrain = self.client.loader.load_model('models/terrain.egg')
        self.client.map.terrain.reparent_to(self.client.render)
        self.client.main_menu.hide()
