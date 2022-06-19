from .bank import MetaClass
from abc import abstractmethod
import logging

log = logging.getLogger(__name__)


class BaseTextCommandHandler(metaclass=MetaClass):
    KEYWORD: str = None
    # number of words in a command, for example "/setname Grzesiek" has 2
    LENGTH: int = 2

    def __init__(self, session, command_vector: list[str]):
        self.session = session
        self.command_vector = command_vector

    def __call__(self):
        self.validate_command()
        self.handle_command()

    @abstractmethod
    def handle_command(self):
        pass

    def validate_command(self):
        if len(self.command_vector) <= self.LENGTH:
            raise Exception(
                f"Not enough words in the passed <{self.command_vector}> command."
            )

