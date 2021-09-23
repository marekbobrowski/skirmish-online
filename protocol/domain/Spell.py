from .base import BaseModel, UInt8


Spells = {
    0: "Some spell 0",
}


class Spell(BaseModel):
    spell = UInt8.customize(accepted_values=Spells)
