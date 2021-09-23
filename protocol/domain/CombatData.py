from .base import BaseModel, ListOf, UInt8


class CombatData(BaseModel):
    spell = UInt8
    hp_change = UInt8
    source = UInt8
    targets = ListOf(UInt8)
