from window_setup import window_setup
from scene.scene import Scene

if __name__ == "__main__":
    # create singleton ShowBase instance
    import core

    # set up window icon, title, size etc.
    window_setup()

    # create singleton ViewManager instance
    from scene import scene_manager
    scene_manager.instance.change_scene_to(Scene.MENU)

    # create singleton NetworkingManager instance
    from networking import networking_manager

    # run
    core.instance.run()
