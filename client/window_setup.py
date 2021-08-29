from panda3d.core import WindowProperties
import assets_dir_config
import core


def window_setup():
    # set up the window icon and cursor appearance
    props = WindowProperties()
    props.set_title('Skirmish Online')
    props.set_size(980, 540)
    props.set_icon_filename(assets_dir_config.assets_dir + 'artwork/icon.ico')
    props.set_cursor_filename(assets_dir_config.assets_dir + 'artwork/cursor.ico')
    core.instance.win.request_properties(props)
    core.instance.disable_mouse()  # disable the default Panda3D mouse controlling system
