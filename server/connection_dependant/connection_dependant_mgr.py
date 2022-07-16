from server.event.event_user import EventUser
from server.event.event import Event
import json
import logging
import sys

log = logging.getLogger(__name__)


class ConnectionDependantManager(EventUser):
    """
    Inherit from this class if your class contains a dictionary that stores objects per connection.
    Inheriting from this class will make sure that proper object will be deleted once a timeout occurs.
    """
    def __init__(self, per_connection_dict):
        super().__init__()
        # dictionary that stores some objects per connection
        self.per_connection_dict = per_connection_dict
        self.accept_event(Event.CLIENT_DISCONNECTION_PUBLISHED, self.handle_timeout)

    def handle_timeout(self, connection):
        """
        Deletes an object for a connection if a timeout occurred.
        """
        if connection in self.per_connection_dict:
            obj = self.per_connection_dict[connection]
            obj.stop_listening_threads()
            del obj
