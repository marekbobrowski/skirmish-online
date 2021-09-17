from .base import BaseModel, UInt8, String


class Animation(BaseModel):
    animation_name = String
    loop = UInt8
