from .queue_subscribers.positon_update import PositionUpdateSubscriber
from .queue_subscribers.new_player import NewPlayerSubscriber
from .queue_subscribers.animation_update import AnimationUpdateSubscriber
from .queue_subscribers.health_change import HealthUpdateSubscriber
from .queue_subscribers.mana_change import ManaUpdateSubscriber
from .queue_subscribers.text_message import TextMessageSubscriber
from .queue_subscribers.name_update import NameUpdateSubscriber
from .queue_subscribers.model_update import ModelUpdateSubscriber
from .queue_subscribers.weapon_update import WeaponUpdateSubscriber
from .queue_subscribers.disconnect import DisconnectSubscriber
from server.connection_dependant.connection_dependant_mgr import ConnectionDependantManager
from server.connection_dependant.connection_dependant import ConnectionDependantObj

from redis import Redis
from direct.distributed.PyDatagram import PyDatagram
import logging


log = logging.getLogger(__name__)


class NotifierManager(ConnectionDependantManager):
    def __init__(self, server):
        """
        Manager, accommodates all notifiers
        """
        self.server = server
        self.notifiers = {}
        super().__init__(per_connection_dict=self.notifiers)

    def new_notifier(self, session, connection):
        """
        Produce new notifier, for session and connection notifying new user
        """
        self.notifiers[connection] = EventNotifier(self.server, session, connection)


class EventNotifier(ConnectionDependantObj):
    def __init__(self, server, session, connection):
        """
        EventNotifier creates sub notifiers, which
        send updates to session user of new events
        """
        self.server = server
        self.session = session
        self.connection = connection

        self.redis = Redis(host="redis")

        self.subsubscribers = [
            PositionUpdateSubscriber(self),
            NewPlayerSubscriber(self),
            AnimationUpdateSubscriber(self),
            HealthUpdateSubscriber(self),
            ManaUpdateSubscriber(self),
            TextMessageSubscriber(self),
            NameUpdateSubscriber(self),
            ModelUpdateSubscriber(self),
            WeaponUpdateSubscriber(self),
            DisconnectSubscriber(self)
        ]
        for subsubscriber in self.subsubscribers:
            subsubscriber.run()

    def notify(self, message):
        """
        Method called by sub notifiers to send message
        """
        if self.session.ready_for_continuous_sync:
            datagram = PyDatagram()
            message.dump(datagram)
            self.server.writer.send(datagram, self.connection)

    def stop_listening_threads(self):
        """
        We don't store any threads in this class.
        """
        pass
