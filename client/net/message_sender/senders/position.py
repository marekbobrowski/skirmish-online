from .base import BaseSender, ServerEvent
from protocol.messages import PosHPRRequest
import time


class PositionSender(BaseSender):
    """
    Position sender
    """

    MANAGED_EVENT = ServerEvent.POSITION_CHANGED
    MESSAGE_CLS = PosHPRRequest

    def handle(self, position):
        """
        Handle new position
        """
        self.send(PosHPRRequest.build(position))
