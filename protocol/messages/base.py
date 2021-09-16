from abc import ABC
from typing import List
from ..domain.base import ObjectBase, UInt8


class Message(ABC):
    ID: UInt8
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
