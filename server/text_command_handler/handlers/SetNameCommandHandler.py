from .base import BaseTextCommandHandler


class SetNameCommandHandler(BaseTextCommandHandler):
    KEYWORD = "/setname"
    LENGTH = 1

    def handle_command(self):
        new_name = self.command_vector[1]
        self.session.player_cache.publish_name_update(new_name)



