import sys

from communication.interlocutor import Interlocutor


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: <python> main.py <server_ip>")
    else:
        server_ip = sys.argv[1]
        interlocutor = Interlocutor()
        print("Connecting...")
        if interlocutor.connect(server_ip):
            print("Connected. Loading assets...")

            # create singleton ShowBase
            from local import core

            from local.ui.ui import Ui
            from local.load_assets import load_assets_to_cache
            from local.world import World
            from local.control.control import Control
            from local.scene import Scene

            load_assets_to_cache()

            world = World()
            scene = Scene()
            ui = Ui()
            control = Control(world, interlocutor)

            lines = interlocutor.get_welcome_message()
            if lines is not None:
                for line in lines:
                    ui.console.add_line(line)
                ui.console.update_view()

            interlocutor.get_world_state()
            interlocutor.begin_sync(world)

            core.instance.run()
