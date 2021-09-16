from .base import Message, UInt8
from ..domain import WelcomeMessage


class WelcomeMessage:
    ID = UInt8(3)
    SCHEMA = [WelcomeMessage]
