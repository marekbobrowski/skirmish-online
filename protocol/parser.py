from .messages import MessagesBank
from .messages.base import Message


class MessageParser:
    def message_by_id(self, _id: int) -> Message:
        return MessagesBank.by_id(_id)

    def parse(self, iterator):
        return self.message_by_id(iterator.get_uint8()).parse(iterator)
