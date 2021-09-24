from .communication.net_client import NetClient
from .local import core
from client.local.section.section_manager import SectionManager
from client.local.section.main.section import MainSection


class Client:
    def __init__(self, server_ip):
        self.net_client = NetClient(server_ip)
        self.section_manager = SectionManager()

    def run(self):
        if self.net_client.connect():
            self.section_manager.switch_to_section(MainSection)

            world_state = self.net_client.get_world_state()
            self.section_manager.active_section.load_state(world_state)

            # self.net_client.send_ready_for_updates()

            # core.instance.run()


