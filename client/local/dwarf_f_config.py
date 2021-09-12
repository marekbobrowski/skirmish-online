from local import asset_names
from local.animation import Animation
from local.subpart import Subpart

from direct.actor.Actor import Actor


def load():

    character = Actor(asset_names.dwarf_f)
    character.make_subpart(Subpart.LEGS, ['Bip01_L_Thigh', 'Bip01_R_Thigh', 'Sheath_L_Bone', 'Bone01'])
    character.make_subpart(Subpart.TORSO, ['Bip01_Spine1'])
    character.set_play_rate(0.2, anim_names[Animation.STAND])

    return character


def get_anim_name(anim):
    return anim_names[anim]


anim_names = {
    Animation.STAND: 'wait_2HS_FDwarf',
    Animation.RUN: 'run_2HS_FDwarf'
}