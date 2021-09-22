from dataclasses import dataclass


@dataclass
class Player:
    id: int
    name: str
    health: int
    model: int
    animation: str
    weapon: int

    x: float
    y: float
    z: float
    h: float
    p: float
    r: float
