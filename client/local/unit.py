from direct.actor.Actor import Actor
from dataclasses import dataclass
from typing import Optional, Any
from protocol.domain import Player


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

    def __init__(self, *args, **kwargs):
        """
        Special use case is initializing
        unit from Player
        """
        if len(args) == 1 and isinstance(args[0], Player):
            player = args[0]
            data = {
                "id": player.id,
                "name": player.name,
                "health": player.health,
                "animation": player.animation,
                "weapon": player.weapon,
            }
            data.update(kwargs)
            super().__init__(**data)
        else:
            super().__init__(*args, **kwargs)
