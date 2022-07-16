from .sub_notifiers.positon_update import PositionUpdateNotifier
from .sub_notifiers.new_player import NewPlayerNotifier
from .sub_notifiers.animation_update import AnimationUpdateNotifier
from .sub_notifiers.health_change import HealthUpdateNotifier
from .sub_notifiers.mana_change import ManaUpdateNotifier
from .sub_notifiers.text_message import TextMessageNotifier
from .sub_notifiers.name_update import NameUpdateNotifier
from .sub_notifiers.model_update import ModelUpdateNotifier
from .sub_notifiers.weapon_update import WeaponUpdateNotifier
from .sub_notifiers.disconnect import DisconnectionNotifier
from .sub_notifiers.combat_data import CombatDataNotifier
from server.connection_dependant.connection_dependant_mgr import ConnectionDependantManager
from server.connection_dependant.connection_dependant import ConnectionDependantObj
from server import config

from redis import Redis
from direct.distributed.PyDatagram import PyDatagram
import logging


log = logging.getLogger(__name__)


class NotifierManager(ConnectionDependantManager):
    def __init__(self, server):
        """
        Accommodates all notifiers (for every connection there's one notifier)
        """
        self.server = server
        self.notifiers = {}
        super().__init__(per_connection_dict=self.notifiers)

    def new_notifier(self, session, connection):
        """
        Produce new notifier for connection
        """
        self.notifiers[connection] = EventNotifier(self.server, session, connection)


class EventNotifier(ConnectionDependantObj):

    def __init__(self, server, session, connection):
        """
        EventNotifier notifies user of the session about some events/changes in the game state, e.g other player's
        animation being changed.

        For every event there's a separate sub-notifier.
        """
        super().__init__()
        self.server = server
        self.session = session
        self.connection = connection

        self.redis = Redis(host=config.redis_host)

        self.sub_notifiers = [
            PositionUpdateNotifier(self),
            NewPlayerNotifier(self),
            AnimationUpdateNotifier(self),
            HealthUpdateNotifier(self),
            ManaUpdateNotifier(self),
            TextMessageNotifier(self),
            NameUpdateNotifier(self),
            ModelUpdateNotifier(self),
            WeaponUpdateNotifier(self),
            DisconnectionNotifier(self),
            CombatDataNotifier(self)
        ]
        for sub_notifier in self.sub_notifiers:
            sub_notifier.start_listening()

    def notify(self, message):
        """
        Method called by sub notifiers to send a message
        """
        if self.session.ready_for_continuous_sync:
            datagram = PyDatagram()
            message.dump(datagram)
            self.server.writer.send(datagram, self.connection)

    def stop_listening_threads(self):
        pass