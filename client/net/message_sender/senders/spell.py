from .base import BaseSender, Event
from protocol.messages import SpellRequest


class SpellSender(BaseSender):
    """
    Sends spell cliecked
    """

    MANAGED_EVENT = Event.CLIENT_SPELL_ATTEMPT
    MESSAGE_CLS = SpellRequest

    def handle(self, ability: int) -> None:
        """
        Sends the spell cliecked
        """
        self.send(SpellRequest.build(ability))
