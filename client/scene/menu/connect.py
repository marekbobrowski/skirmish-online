from threading import Thread
from networking import networking_manager
from scene import scene_manager
from scene.scene import Scene


def connection_control(server_ip):
    scene_manager.instance.show_dialog(text='Connecting...', button_text='Cancel',
                                       button_command=None)
    connected = networking_manager.instance.connect(server_ip)
    if connected:
        scene_manager.instance.show_dialog('Connected! Loading models...')
        scene_manager.instance.load_scene(Scene.CHARACTER_MENU)
        scene_manager.instance.change_scene_to(Scene.CHARACTER_MENU)
        scene_manager.instance.hide_dialog()
    else:
        scene_manager.instance.show_dialog(text='Failed to connect.', button_text='Return',
                                           button_command=None)


def connect_attempt(server_ip):
    if not networking_manager.instance.is_connecting:
        networking_manager.instance.is_connecting = True
        # running this function in new thread so connecting & model loading don't block the main thread
        Thread(target=connection_control, args=(server_ip,)).start()
