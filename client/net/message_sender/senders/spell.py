from .base import BaseSender
from client.local.client_event import ClientEvent
from protocol.messages import SpellRequest


class SpellSender(BaseSender):
    """
    Sends spell cliecked
    """

    MANAGED_EVENT = ClientEvent.SPELL_ATTEMPT
    MESSAGE_CLS = SpellRequest

    def handle(self, ability: int) -> None:
        """
        Sends the spell cliecked
        """
        self.send(SpellRequest.build(ability))
