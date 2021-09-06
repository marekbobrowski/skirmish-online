from communication.networking import Networking
from local import core
from local.ui.ui import Ui
from local.load_assets import load_assets_to_cache
from local.world import World
from local.control.control import Control
from local.scene.scene import Scene

import sys

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: <python> main.py <server_ip>")
    else:
        server_ip = sys.argv[1]
        networking = Networking()
        print("Connecting...")
        if networking.connect(server_ip):
            print("Connected. Loading assets...")

            load_assets_to_cache()

            world = World()
            scene = Scene()
            ui = Ui()
            control = Control()

            networking.load_world_state(world, scene)
            networking.send_ready_for_updates()
            networking.begin_sync()

            control.enable(scene.characters[world.player.id], core.instance.camera)
            core.instance.run()
