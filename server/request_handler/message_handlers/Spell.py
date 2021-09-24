from .base import MessageHandler
from protocol import messages
from ...spell_handler.handler import SpellHandler


class SpellMessageHandler(MessageHandler):
    handled_message = messages.SpellRequest
    response_message = messages.CombatDataResponse

    def __call__(self):
        """
        Handle the spell. This procedure creates handler for
        the spell_data and executes it
        """
        spell_data = self.message.data
        handler = SpellHandler(spell_data, self.session)
        combat_data = handler()
        return messages.CombatDataResponse(combat_data)
