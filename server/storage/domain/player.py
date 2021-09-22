from dataclasses import dataclass


@dataclass
class PlayerPositionUpdate:
    id: int
    x: float
    y: float
    z: float
    h: float
    p: float
    r: float


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

    def update_position(self, position: PlayerPositionUpdate):
        self.x = position.x
        self.y = position.y
        self.z = position.z
        self.h = position.h
        self.p = position.p
        self.r = position.r
