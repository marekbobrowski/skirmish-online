from .base import RegularStateUpdaterBase
import logging

log = logging.getLogger(__name__)


class HealthRegenerator(RegularStateUpdaterBase):
    INTERVAL: int = 1
    AMOUNT: int = 2

    def update_state(self):
        player_id_list = [self.session.player.id]
        self.session.player_cache.publish_health_update(player_id_list, -self.AMOUNT)
