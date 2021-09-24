from .base import BaseModel, UInt8, String, Float64


class Player(BaseModel):
    id = UInt8
    name = String
    health = UInt8
    model = UInt8
    animation = String
    weapon = UInt8

    x = Float64
    y = Float64
    z = Float64
    h = Float64
    p = Float64
    r = Float64


class PlayerPosHPR(BaseModel):
    x = Float64
    y = Float64
    z = Float64
    h = Float64
    p = Float64
    r = Float64


class PlayerIdPosHPR(BaseModel):
    id = UInt8
    x = Float64
    y = Float64
    z = Float64
    h = Float64
    p = Float64
    r = Float64
