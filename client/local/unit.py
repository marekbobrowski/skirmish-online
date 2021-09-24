from direct.actor.Actor import Actor
from protocol.domain import Player
from dataclasses import dataclass
from typing import Optional, Any


@dataclass
class Unit:
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
            "animation": player.animation,
            "weapon": player.weapon,
        }
        return cls(**data)
