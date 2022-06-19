from abc import abstractmethod
from threading import Thread
from time import sleep


class RegularStateUpdaterBase:
    INTERVAL: int = 5
    AMOUNT: int = 5

    def __init__(self, session):
        self.session = session
        self.thread = None

    @abstractmethod
    def update_state(self):
        pass

    def update_state_loop(self):
        while True:
            if self.session.player is not None:
                self.update_state()
            sleep(self.INTERVAL)

    def start_regular_update(self):
        """
        Runs a thread in which certain parts of unit state (e. g. health) will be regularly updated.
        """
        self.thread = Thread(target=self.update_state_loop, daemon=True)
        self.thread.start()
