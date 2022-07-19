from .base import UInt8, String, BaseModel, Float64


class ScaleUpdate(BaseModel):
    id = UInt8
    scale = Float64
