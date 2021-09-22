from .base import Message, MessageType, UInt8
from ..domain import Animation


class AnimationRequest(Message):
    ID = UInt8(51)
    SCHEMA = Animation
    TYPE = MessageType.request
