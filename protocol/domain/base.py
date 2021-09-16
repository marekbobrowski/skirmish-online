from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import overload


class ObjectBase(ABC):
    @classmethod
    @abstractmethod
    def parse(cls, iterator) -> "ObjectBase":
        pass

    @abstractmethod
    def dump(self, datagram) -> None:
        pass


@dataclass
class BaseModel(ObjectBase, ABC):
    @classmethod
    @overload
    def parse(cls, iterator) -> "BaseModel":
        kwargs = {}
        for field in cls.__dataclass_fields__.values():
            kwargs[field.name] = field.type.parse(iterator)
        return cls(**kwargs)

    @overload
    def dump(self, datagram) -> None:
        for field in self.__dataclass_fields__.values():
            getattr(self, field.name).dump(datagram)


class UInt8(ObjectBase, int):
    @classmethod
    @overload
    def parse(cls, iterator) -> "UInt8":
        return cls(iterator.get_uint8())

    @overload
    def dump(self, datagram) -> None:
        datagram.add_uint8(self.__int__())


class String(ObjectBase, str):
    @classmethod
    @overload
    def parse(cls, iterator) -> "String":
        return cls(iterator.get_string())

    @overload
    def dump(self, datagram) -> None:
        datagram.add_string(self.__str__())


class MultilineString(String):
    @classmethod
    @overload
    def parse(cls, iterator) -> "MultilineString":
        lines = iterator.get_uint8()
        value = "\n".join((iterator.get_string() for i in len(lines)))
        return cls(value)

    @overload
    def dump(self, datagram) -> None:
        lines = self.__str__().splitlines()
        datagram.add_uint8(len(lines))
        for line in lines:
            datagram.add_string(line)

