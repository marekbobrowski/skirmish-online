from client.local import core
from client.event import Event
from direct.showbase.DirectObject import DirectObject
from ..utils.frame import Frame, Anchor
from client.local.section.main.ui.action_bar.cooldown_trackers.base import CooldownTrackerBase
from .cooldown_trackers import TrackerSpell1, TrackerSpell2, TrackerSpell3, TrackerSpell4
from direct.task.Task import Task


class ActionBar(DirectObject):
    """
    GUI element responsible for displaying available spells and their cooldowns.
    """
    N_SLOTS = 9

    def __init__(self, node):
        DirectObject.__init__(self)
        self.accept(Event.COMBAT_DATA_RECEIVED, self.handle_combat_data_received)
        self.node = node.attach_new_node("action bar")
        self.frame = Frame(node=self.node,
                           anchor=Anchor.CENTER,
                           color=(0, 0, 0, 0.6),
                           x_offset=0,
                           y_offset=0.01,
                           width=0.25,
                           height=0.05)

        x_offset = 0.026
        spell_slot_width = 0.025
        padding = 0.003
        y_offset = 0.049
        self.spell_slots = []
        slot_classes = [TrackerSpell1, TrackerSpell2, TrackerSpell3, TrackerSpell4]
        for i in range(self.N_SLOTS):
            if i in range(0, len(slot_classes)):
                self.spell_slots.append(slot_classes[i](node=self.frame.node,
                                                        x_offset=x_offset,
                                                        y_offset=y_offset,
                                                        parent_frame=None))
            else:
                self.spell_slots.append(CooldownTrackerBase(node=self.frame.node,
                                                            x_offset=x_offset,
                                                            y_offset=y_offset,
                                                            parent_frame=None))
            # self.spell_slots.append(SpellSlot2(node=self.frame.node,
            #                                       x_offset=x_offset,
            #                                       y_offset=y_offset + 2 * padding,
            #                                       parent_frame=None))
            x_offset += spell_slot_width + padding

        if type(self) != CooldownTrackerBase:
            self.set_cooldown_tracking(0, 1)
            self.set_cooldown_tracking(1, 2)
            self.set_cooldown_tracking(2, 3)
            self.set_cooldown_tracking(3, 4)

    def set_cooldown_tracking(self, slot_number, spell_cooldown):
        slot = self.spell_slots[slot_number]
        slot.default_cooldown = spell_cooldown
        slot.temp_cooldown = spell_cooldown
        task = Task(slot.update_cooldown_view, "update cooldown view")
        core.instance.task_mgr.add(task, extraArgs=[task, spell_cooldown])

    def handle_combat_data_received(self, *args):
        spell_id = args[0]
        hp_change = args[1]
        if hp_change == 0:
            return

        slot = self.spell_slots[spell_id]

        # trigger cooldown for the spell
        task = Task(slot.update_cooldown_view, "update cooldown view")
        core.instance.task_mgr.add(task, extraArgs=[task, slot.default_cooldown])

        # trigger global cooldown
        # so that spells aren't used more often than 1 second
        for i, slot in enumerate(self.spell_slots):
            if i != spell_id and not type(self.spell_slots[i]) == CooldownTrackerBase:
                if slot.remaining_time < 1:
                    task = Task(slot.update_cooldown_view, "update cooldown view")
                    slot.remaining_time = 1
                    core.instance.task_mgr.add(task, extraArgs=[task, 1])



