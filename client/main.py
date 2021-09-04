from communication.interlocutor import Interlocutor

import sys

from panda3d.core import Vec3

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
            scene = Scene(world)

            ui = Ui(interlocutor, world)
            control = Control(world, scene, interlocutor)

            lines = interlocutor.get_welcome_message()
            ui.console.add_lines(lines)
            ui.console.update_view()

            iterator, datagram = interlocutor.get_world_state()
            world.load_world_state(iterator, datagram)

            scene.set_up_camera()

            control.enable(world.player.character, core.instance.camera)
            control.cam_ctrl.attach_to(world.player.character, Vec3(0, 0, 1))
            control.cam_ctrl.zoom_out(4)

            interlocutor.send_ready_for_updates()
            interlocutor.begin_sync(world)

            interlocutor.plug_console(ui.console)

            core.instance.disable_mouse()
            core.instance.run()
