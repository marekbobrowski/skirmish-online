from communication.interlocutor import Interlocutor

import sys

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
            from local.scene.scene import Scene

            load_assets_to_cache()

            world = World()
            scene = Scene()
            ui = Ui()
            control = Control()

            interlocutor.get_welcome_message()
            interlocutor.get_world_state()

            control.enable(scene.characters[world.player.id],
                           core.instance.camera)

            interlocutor.send_ready_for_updates()
            interlocutor.begin_sync()

            core.instance.disable_mouse()
            core.instance.run()
