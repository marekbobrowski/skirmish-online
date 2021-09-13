from local import asset_names
from local.animation import Animation
from local.subpart import Subpart

from direct.actor.Actor import Actor


def load():
    character = Actor(asset_names.elf)
    character.make_subpart(
        Subpart.LEGS, ["Bip01_L_Thigh", "Bip01_R_Thigh", "Sheath_L_Bone", "Bone01"]
    )
    character.make_subpart(Subpart.TORSO, ["Bip01_Spine1"])
    character.set_play_rate(0.2, anim_names[Animation.STAND])
    character.set_play_rate(3, anim_names[Animation.MELEE_ATTACK_1])
    # character.list_joints()
    # print(character.get_anim_names())
    return character


def get_anim_name(anim):
    return anim_names[anim]


anim_names = {
    Animation.STAND: "wait_2HS_FElf",
    Animation.RUN: "run_2HS_FElf",
    Animation.MELEE_ATTACK_1: "Atk02_2HS_FElf",
}
