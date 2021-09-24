from client.local.assets import asset_names
from client.local.model_config.actor_config.animation import Animation
from client.local.subpart import Subpart

from direct.actor.Actor import Actor


def load():
    character = Actor(asset_names.dark_elf)
    character.make_subpart(
        Subpart.LEGS, ["Bip01_L_Thigh", "Bip01_R_Thigh", "skirt_Bone01", "Bone01"]
    )
    character.make_subpart(Subpart.TORSO, ["Bip01_Spine1"])
    character.set_play_rate(3, anim_names[Animation.MELEE_ATTACK_1])
    character.set_play_rate(3, anim_names[Animation.MELEE_ATTACK_2])
    character.set_play_rate(3, anim_names[Animation.MAGIC_ATTACK_1])
    return character


def get_anim_name(anim):
    return anim_names[anim]


anim_names = {
    Animation.STAND: "wait_2HS_FDarkElf",
    Animation.RUN: "run_2HS_FDarkElf",
    Animation.MELEE_ATTACK_1: "Atk01_2HS_FDarkElf",
    Animation.MELEE_ATTACK_2: "SpAtk001_2HS_FDarkElf",
    Animation.MAGIC_ATTACK_1: "CastMid_FDarkElf",
}
