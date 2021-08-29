from threading import Thread
from scene import scene_manager
from networking import networking_manager
from scene.scene import Scene


def join_skirmish_attempt(player_name, selected_class):
    """
    Attempts to join the skirmish.
    """
    if not scene_manager.instance.joining_skirmish:
        scene_manager.instance.joining_skirmish = True
        # running this function in new thread so that
        # client-server communication and model loading don't block the main thread
        Thread(target=join_skirmish, args=(player_name, selected_class,)).start()


def join_skirmish(player_name, selected_class):
    """
    Joins the skirmish by asking the server for a pass (the server check's if the nickname is not taken)
    and if everything's fine, loads and enters the skirmish scene.
    """
    scene_manager.instance.show_dialog('Asking for a pass...')
    passed = networking_manager.instance.ask_for_pass(player_name, selected_class)
    if passed:
        scene_manager.instance.hide_dialog()
        scene_manager.instance.change_scene_to(Scene.LOADING_SCREEN)
        scene_manager.instance.load_scene(Scene.SKIRMISH)
        scene_manager.instance.change_scene_to(Scene.SKIRMISH)
    else:
        scene_manager.instance.show_dialog('This nickname is already in use.\nPlease change it.')
        networking_manager.instance.joining_skirmish = False
