from typing import List
from enum import Enum
import dataclasses
from ..domain.base import ObjectBase, UInt8


class MessagesBank:
    class RequestMessagesBank:
        messages = []
        messages_by_id = {}

    class ResponseMessagesBank:
        messages = []
        messages_by_id = {}

    @classmethod
    def register(cls, message_cls: "Message") -> None:
        if message_cls.TYPE is None:
            return

        bank = cls.bank_for_type(message_cls.TYPE)

        if message_cls.ID in bank.messages_by_id:
            raise Exception(
                f"message_cls {bank.messages_by_id[message_cls.ID]} and {message_cls} share the same ID!"
            )

        bank.messages.append(message_cls)
        bank.messages_by_id[message_cls.ID] = message_cls

    @classmethod
    def bank_for_type(cls, type_: "MessageType") -> type:
        return {
            MessageType.request: cls.RequestMessagesBank,
            MessageType.response: cls.ResponseMessagesBank,
        }[type_]

    @classmethod
    def by_id(cls, _id: int, type_: "MessageType") -> "Message":
        bank = cls.bank_for_type(type_)
        return bank.messages_by_id[_id]


class MetaClass(type):
    def __new__(cls, clsname, bases, attrs):
        newclass = super(MetaClass, cls).__new__(cls, clsname, bases, attrs)
        MessagesBank.register(newclass)
        return newclass


class MessageType(Enum):
    request = "Request"
    response = "Response"


class Message(metaclass=MetaClass):
    ID: UInt8
    SCHEMA: List[ObjectBase]
    TYPE: MessageType = None

    def __init__(self, data: List[ObjectBase]):
        self.data = data

    @classmethod
    def build(cls, values=None, **kwargs) -> "Message":
        if values is None:
            values = [kwargs]

        data = []

        if not isinstance(values, (tuple, list)):
            values = [values]

        for model, value in zip(cls.SCHEMA, values):
            if isinstance(value, model):
                data.append(value)
            elif isinstance(value, (tuple, list)):
                data.append(model.build(*value))
            elif isinstance(value, dict):
                data.append(model.build(**value))
            elif dataclasses.is_dataclass(value):
                data.append(model.from_dataclass(value))
            else:
                data.append(model.build(value))
                # will raise if incompatibile
        return cls(data)

    @classmethod
    def parse(cls, iterator) -> "Message":
        data = [model.parse(iterator) for model in cls.SCHEMA]
        return cls(data)

    def dump(self, datagram) -> None:
        self.ID.dump(datagram)
        for obj in self.data:
            obj.dump(datagram)
