from direct.actor.Actor import Actor
from protocol.domain import Player
from dataclasses import dataclass
from typing import Optional, Any


@dataclass
class Unit:
    x: float
    y: float
    z: float
    h: float
    p: float
    r: float
    id: int = -1
    name: str = "Unknown"
    health: int = 0
    model: Optional[int] = None
    animation: Optional[str] = None
    weapon: Optional[str] = None
    base_node: Optional[Any] = None
    weapon_node: Optional[Any] = None
    actor: Optional[Actor] = None

    @classmethod
    def from_player(cls, player):
        """
        Special use case is initializing
        unit from Player
        """
        data = {
            "id": player.id,
            "name": player.name,
            "health": player.health,
            "model": player.model,
            "animation": player.animation,
            "weapon": player.weapon,
            "x": player.x,
            "y": player.y,
            "z": player.z,
            "h": player.h,
            "p": player.p,
            "r": player.r,
        }
        return cls(**data)
