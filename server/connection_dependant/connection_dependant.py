from abc import abstractmethod


class ConnectionDependantObj:
    """
    Objects that are created per connection might spawn threads for event listening.
    We need to make sure that we stop these threads once the connection ends / timeout occurs.
    """
    @abstractmethod
    def stop_listening_threads(self):
        pass
