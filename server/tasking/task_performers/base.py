from abc import abstractmethod
from threading import Thread
from time import sleep


class TaskPerformerBase:
    INTERVAL: int = 5
    AMOUNT: int = 5

    def __init__(self, session):
        self.session = session
        self.thread = None

    @abstractmethod
    def task_tick(self):
        pass

    def perform_task(self):
        while True:
            self.task_tick()
            sleep(self.INTERVAL)

    def start_task(self):
        """
        Runs a thread in which the task is performed regularly, with specified interval.
        """
        self.thread = Thread(target=self.perform_task, daemon=True)
        self.thread.start()
