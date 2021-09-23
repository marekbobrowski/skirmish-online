from .base import MessageHandler
from protocol import messages


class SpellHandler(MessageHandler):
    handled_message = messages.SpellRequest
    response_message = None

    def handle_message(self):
        """
        Publish event of spell being used
        """
        spell_data = self.message.data
        self.session.set_spell(spell_data)

    def build_response(self):
        """
        Responds with CombatData
        """
        pass
