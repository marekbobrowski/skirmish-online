from .base import BaseSender, Event
from protocol.messages import PosHPRRequest
import time


class PositionSender(BaseSender):
    """
    Position sender
    """
    MANAGED_EVENT = Event.POSITION_CHANGED
    MESSAGE_CLS = PosHPRRequest

    def handle(self, position):
        """
        Handle new position
        """
        self.send(
            PosHPRRequest.build(
                position
            )
        )
