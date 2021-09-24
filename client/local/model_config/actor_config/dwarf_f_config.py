from client.local.assets import asset_names
from client.local.model_config.actor_config.animation import Animation

from direct.actor.Actor import Actor


def load():

    character = Actor(asset_names.dwarf_f)
    character.set_play_rate(0.2, anim_names[Animation.STAND])
    character.set_play_rate(3, anim_names[Animation.MELEE_ATTACK_1])
    character.set_play_rate(3, anim_names[Animation.MELEE_ATTACK_2])
    character.set_play_rate(3, anim_names[Animation.MAGIC_ATTACK_1])
    return character


def get_anim_name(anim):
    return anim_names[anim]


anim_names = {
    Animation.STAND: "wait_2HS_FDwarf",
    Animation.RUN: "run_2HS_FDwarf",
    Animation.MELEE_ATTACK_1: "Atk01_2HS_FDwarf",
    Animation.MELEE_ATTACK_2: "SpAtk001_2HS_FDwarf",
    Animation.MAGIC_ATTACK_1: "CastMid_A_FDwarf",
}
