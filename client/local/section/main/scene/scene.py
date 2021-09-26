from ..state.state import MainSectionState
from client.local import core
from client.local.model_config.actor_config import actor_config
from client.local.model_config.weapon_config import weapon_config
from client.local.assets import asset_names as assets
from client.event import Event
from client.local.model_config.actor_config.animation import Animation
from client.local.section.main.ui.floating_bars import FloatingBars
from panda3d.core import PointLight, AmbientLight
from direct.showbase.DirectObject import DirectObject
from direct.task.Task import Task
from ..state.unit_interpolator import UnitInterpolator


class MainSectionScene(DirectObject):
    def __init__(self, state: MainSectionState):
        DirectObject.__init__(self)
        self.state = state
        self.node = core.instance.render.attach_new_node("section node")

        # section has to handle the event first, before the floating bars
        self.accept(Event.LOCAL_NEW_UNIT, self.handle_local_new_unit)
        self.accept(Event.LOCAL_UNIT_POS_ROT_CHANGED, self.handle_unit_pos_hpr_changed)
        self.accept(
            Event.PLAYER_CHANGED_ANIMATION, self.handle_player_changed_animation
        )
        self.accept(Event.NAME_CHANGED, self.handle_name_changed)
        self.accept(Event.MODEL_CHANGED, self.handle_model_changed)
        self.accept(Event.WEAPON_CHANGED, self.handle_weapon_changed)

        self.floating_bars = FloatingBars(self.state)

        # those will be parented to the section graph so need to keep the references
        skybox = core.instance.loader.loadModel(assets.skybox)
        skybox.set_scale(100)
        skybox.reparent_to(core.instance.camera)
        skybox.set_compass(core.instance.render)

        terrain = core.instance.loader.loadModel(assets.arena)
        terrain.reparent_to(self.node)
        terrain.set_scale(10)
        terrain.set_z(0.82)

        plight = PointLight("plight")
        plight.setColor((5, 5, 5, 0))
        plight_node_path = self.node.attachNewNode(plight)
        plight_node_path.setPos(20, 0, 0)
        core.instance.render.setLight(plight_node_path)

        alight = AmbientLight("alight")
        alight.setColor((1, 1, 1, 0))
        alight_node_path = self.node.attachNewNode(alight)
        alight_node_path.setPos(20, 0, 0)
        core.instance.render.setLight(alight_node_path)

    def show(self) -> None:
        self.node.show()

    def hide(self) -> None:
        self.node.hide()

    def handle_local_new_unit(self, *args):
        unit = args[0]
        self.spawn_unit(unit)

    def handle_unit_pos_hpr_changed(self, *args):
        return
        unit = args[0]
        if unit is not None:
            self.move_rotate_character(
                unit, unit.x, unit.y, unit.z, unit.h, unit.p, unit.r
            )

    def handle_player_changed_animation(self, *args):
        unit = self.state.units_by_id.get(args[0], None)
        self.change_animation(unit, args[1], args[2])

    def handle_name_changed(self, id_, name):
        self.state.units_by_id.get(id_).name = name

    def spawn_unit(self, unit):
        unit.actor = actor_config.load(unit.model)
        weapon = weapon_config.load(unit.weapon)
        self.equip_weapon(unit, weapon)
        self.change_animation(unit, unit.animation, 1)
        unit.base_node = self.node.attach_new_node("actor base node")
        unit.base_node.set_pos_hpr(unit.x, unit.y, unit.z, unit.h, unit.p, unit.r)
        unit.actor.reparent_to(unit.base_node)
        unit.actor.set_blend(frameBlend=True)
        if unit.id != self.state.player_id:
            unit.interpolator = UnitInterpolator(unit)
            unit.interpolator.update()
            task = Task(self.update_position_task)
            core.instance.task_mgr.add(
                task, f"interpolate{unit}", extraArgs=[unit, task]
            )

    def move_rotate_character(self, unit, x, y, z, h, p, r):
        unit.base_node.set_pos_hpr(x, y, z, h, p, r)

    def change_animation(self, unit, animation, loop):
        animation = actor_config.get_anim_name(unit.model, animation)
        if loop:
            unit.actor.loop(animation)
        else:
            unit.actor.play(animation)

    def equip_weapon(self, unit, weapon):
        unit.hand_node = unit.actor.expose_joint(None, "modelRoot", "Weapon_R_Bone")
        weapon.reparent_to(unit.hand_node)
        unit.weapon_node = weapon

    def handle_model_changed(self, args):
        unit = self.state.units_by_id.get(args.player_id, None)
        unit.model = args.model_id
        unit.actor.removePart("modelRoot")
        unit.actor = actor_config.load(unit.model)
        unit.actor.reparent_to(unit.base_node)
        self.change_animation(unit, Animation.STAND, 1)
        weapon = weapon_config.load(unit.weapon)
        self.equip_weapon(unit, weapon)

    def handle_weapon_changed(self, args):
        self.change_weapon(args.player_id, args.weapon_id)

    def change_weapon(self, player_id, weapon_id):
        unit = self.state.units_by_id.get(player_id, None)
        if unit is not None:
            unit.weapon = weapon_id
            unit.weapon_node.detach_node()
            unit.weapon_node = weapon_config.load(unit.weapon)
            unit.weapon_node.reparent_to(unit.hand_node)

    def update_position_task(self, unit, task):
        unit.interpolator.interpolate()
        return Task.cont
