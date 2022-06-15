from .queue_subscribers.positon_update import PositionUpdateSubscriber
from .queue_subscribers.new_player import NewPlayerSubscriber
from .queue_subscribers.animation_update import AnimationUpdateSubscriber
from .queue_subscribers.health_change import HealthUpdateSubscriber
from .queue_subscribers.text_message import TextMessageSubscriber
from .queue_subscribers.name_update import NameUpdateSubscriber
from redis import Redis
from direct.distributed.PyDatagram import PyDatagram
import logging


log = logging.getLogger(__name__)


class NotifierManager:
    def __init__(self, server):
        """
        Manager, accomodates all notifiers
        """
        self.server = server
        self.handers = {}

    def new_notifier(self, session, connection):
        """
        Produce new notifier, for session and connection notifying new user
        """
        self.handers[connection] = EventNotifier(self.server, session, connection)


class EventNotifier:
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
            TextMessageSubscriber(self),
            NameUpdateSubscriber(self),
        ]
        for subsubscriber in self.subsubscribers:
            subsubscriber.run()

    def notify(self, message):
        """
        Method called by sub notifiers to send message
        """
        datagram = PyDatagram()
        message.dump(datagram)
        self.server.writer.send(datagram, self.connection)
