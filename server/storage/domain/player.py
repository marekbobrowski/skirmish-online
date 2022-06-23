from dataclasses import dataclass
from typing import Optional


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
class PlayerAnimationUpdate:
    id: int
    animation_name: str
    loop: int


@dataclass
class Player:
    id: int
    name: str
    health: int
    mana: int
    model: int
    animation: str
    loop: int
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

    def update_animation(self, animation: PlayerAnimationUpdate):
        self.animation = animation.animation_name
        self.loop = animation.loop
