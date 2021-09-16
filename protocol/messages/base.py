from typing import List
from ..domain.base import ObjectBase, UInt8


class MessagesBank:
    messages = []
    messages_by_id = {}

    @classmethod
    def register(cls, message_cls: "Message") -> None:
        if message_cls.ID is None:
            return

        if message_cls.ID in cls.messages_by_id:
            raise Exception(
                f"message_cls {cls.messages_by_id[message_cls.ID]} and {message_cls} share the same ID!"
            )

        cls.messages.append(message_cls)
        cls.messages_by_id[message_cls.ID] = message_cls

    @classmethod
    def by_id(cls, _id: int) -> "Message":
        return cls.messages_by_id[_id]


class MetaClass(type):
    def __new__(cls, clsname, bases, attrs):
        newclass = super(MetaClass, cls).__new__(cls, clsname, bases, attrs)
        MessagesBank.register(newclass)
        return newclass


class Message(metaclass=MetaClass):
    ID: UInt8 = None
    SCHEMA: List[ObjectBase]

    def __init__(self, data: List[ObjectBase]):
        self.data = data

    @classmethod
    def parse(cls, iterator) -> "Message":
        data = [model.parse(iterator) for model in cls.SCHEMA]
        return cls(data)

    def dump(self, datagram) -> None:
        self.ID.dump(datagram)
        for obj in self.data:
            obj.dump(datagram)
