from .communication.net_client import NetClient
from .local import core
from .local.ui import Ui
from .local.load_assets import load_assets_to_cache
from .local.control import Control
from .local.world import World

import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: <python> main.py <server_ip>")
    else:
        server_ip = sys.argv[1]
        net_client = NetClient()
        print("Connecting...")
        if net_client.connect(server_ip):
            print("Connected. Loading assets...")

            load_assets_to_cache()

            world = World()
            ui = Ui(world.units)

            net_client.load_world_state(world)
            net_client.send_ready_for_updates()

            main_player = world.units[world.main_player_id]
            control = Control(main_player, core.instance.camera)
            control.enable(world.node)
            net_client.begin_sync(control.actor_control.actor, world.node)
            core.instance.run()
