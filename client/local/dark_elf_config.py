from local import asset_names
from local.animation import Animation
from local.subpart import Subpart

from direct.actor.Actor import Actor


def load():
    character = Actor(asset_names.dark_elf)
    character.make_subpart(Subpart.LEGS, ['Bip01_L_Thigh', 'Bip01_R_Thigh', 'skirt_Bone01', 'Bone01'])
    character.make_subpart(Subpart.TORSO, ['Bip01_Spine1'])
    return character


def get_anim_name(anim):
    return anim_names[anim]


anim_names = {
    Animation.STAND: 'wait_2HS_FDarkElf',
    Animation.RUN: 'run_2HS_FDarkElf'
}
