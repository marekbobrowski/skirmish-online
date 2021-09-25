from .net.net_client import NetClient
from .local import core
from client.local.section.section_manager import SectionManager
from client.local.section.main.section import MainSection


class Client:
    STARTUP_SECTION = MainSection

    def __init__(self, server_ip):
        self.net_client = NetClient(server_ip)
        self.section_manager = SectionManager()

    def run(self):
        if self.net_client.connect():
            self.basic_configuration()

            section = self.section_manager.switch_to_section(Client.STARTUP_SECTION)
            section.load_state(
                self.net_client.section_state_fetcher.get_main_section_state()
            )
            section.post_state_setup()

            self.net_client.send_ready_for_updates()
            self.net_client.begin_sync_with_server()

            core.instance.run()

    def basic_configuration(self):
        core.instance.disable_mouse()
        # TODO: set icon, window name etc.
