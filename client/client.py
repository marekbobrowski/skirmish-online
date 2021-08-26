import core
from window_setup import window_setup
from scene.scene_manager import SceneManager
from networking.networking_manager import NetworkingManager

if __name__ == "__main__":
    window_setup()

    scene_manager = SceneManager()
    scene_manager.change_scene_to(0)

    networking_manager = NetworkingManager()

    core.instance.run()
