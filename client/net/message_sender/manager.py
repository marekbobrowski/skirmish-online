from .senders.animation import AnimationSender
from .senders.spell import SpellSender
from .senders.text_message import TextMessageSender

from .updaters.position import PositionUpdater


class MessageSendersManager:
    def __init__(self, manager):
        """
        This class initializes senders
        """
        self.manager = manager
        self.senders = [
            AnimationSender(manager),
            SpellSender(manager),
            TextMessageSender(manager),
        ]
        self.updaters = [
            PositionUpdater(manager),
        ]
