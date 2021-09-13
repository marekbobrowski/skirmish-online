from local import asset_names
from local.animation import Animation
from local.subpart import Subpart

from direct.actor.Actor import Actor


def load():

    character = Actor(asset_names.kamael)
    character.make_subpart(
        Subpart.LEGS, ["Bip01_L_Thigh", "Bip01_R_Thigh", "Sheath_L_Bone"]
    )
    character.make_subpart(Subpart.TORSO, ["Bip01_Spine1"])
    character.set_play_rate(3, anim_names[Animation.MELEE_ATTACK_1])
    # character.list_joints()
    # print(character.get_anim_names())

    return character


def get_anim_name(anim):
    return anim_names[anim]


anim_names = {
    Animation.STAND: "wait_2HS_MKamael",
    Animation.RUN: "run_2HS_MKamael",
    Animation.MELEE_ATTACK_1: "Atk01_2HS_MKamael",
}
