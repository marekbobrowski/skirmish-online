from local import asset_names
from local.model_config.animation import Animation
from local.model_config.subpart import Subpart

from direct.actor.Actor import Actor


def load():
    character = Actor(asset_names.night_elf)
    character.load_anims(
        {
            Animation.STAND: asset_names.night_elf_stand,
            Animation.RUN: asset_names.night_elf_run
        }
    )
    character.make_subpart(Subpart.LEGS, ["nelf_Bone3_SpineLow"])
    character.make_subpart(Subpart.TORSO, ["nelf_Bone4_Waist"])
    return character
