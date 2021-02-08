from scenes.skirmish.quick_menu import QuickMenu


class Interface:
    def __init__(self, skirmish):
        self.skirmish = skirmish
        self.core = skirmish.core
        self.node = skirmish.node_2d.attach_new_node("skirmish interface node")
        self.submodules = [QuickMenu(self)]

    def load(self):
        self.submodules[0].node.hide()
        for submodule in self.submodules:
            submodule.load()

    def update_player(self):
        pass
