from abc import abstractmethod
from typing import List, Dict, Any
import inspect
import datetime


class ObjectBase:
    METADATA = {
        "required": True,
        "default": None,
    }

    @classmethod
    def customize(cls, **kwargs):
        custom_metadata = dict(**cls.METADATA)
        custom_metadata.update(kwargs)

        class Customized(cls):
            METADATA = custom_metadata

        return Customized

    @classmethod
    @abstractmethod
    def parse(cls, iterator) -> "ObjectBase":
        pass

    @abstractmethod
    def dump(self, datagram) -> None:
        pass

    @classmethod
    def build(cls, *args, **kwargs) -> "ObjectBase":
        return cls(*args, **kwargs)

    @classmethod
    @abstractmethod
    def dump_default(cls, datagram) -> None:
        pass

    @abstractmethod
    def _json(self) -> Any:
        pass


class BaseModel(ObjectBase):
    def __init__(self, *args, **kwargs):
        fields = self.get_fields()
        for name in kwargs:
            fields.pop(name)

        kwargs.update(dict(zip(fields.keys(), args)))

        fields = self.get_fields()

        for name, value in kwargs.items():
            if value is not None:
                setattr(self, name, fields[name](value))
            else:
                assert fields[name].METADATA["required"] is False
                setattr(self, name, None)

    @classmethod
    def get_fields(cls) -> "List[ObjectBase]":
        fields = {}
        for name, type_ in cls.__dict__.items():
            if inspect.isclass(type_) and issubclass(type_, ObjectBase):
                fields[name] = type_
        return fields

    def _json(self) -> Dict:
        result = {}
        for name, type_ in self.get_fields().items():
            value = getattr(self, name)
            if value is not None and not inspect.isclass(value):
                result[name] = value._json()
            else:
                result[name] = None
        return result

    @classmethod
    def parse(cls, iterator) -> "BaseModel":
        kwargs = {}
        for name, type_ in cls.get_fields().items():
            kwargs[name] = type_.parse(iterator)
        return cls.build(**kwargs)

    def dump(self, datagram) -> None:
        for name, type_ in self.get_fields().items():
            value = getattr(self, name)
            if value is not None and not inspect.isclass(value):
                value.dump(datagram)
            else:
                type_.dump_default(datagram)

    @classmethod
    def dump_default(cls, datagram) -> None:
        for type_ in cls.get_fields().values():
            type_.dump_default(datagram)


class UInt8(ObjectBase, int):
    @classmethod
    def parse(cls, iterator) -> "UInt8":
        return cls.build(iterator.get_uint8())

    def dump(self, datagram) -> None:
        datagram.add_uint8(self.__int__())

    @classmethod
    def dump_default(cls, datagram) -> None:
        datagram.add_uint8(0)

    def _json(self) -> int:
        return self.__int__()


class Float64(ObjectBase, float):
    @classmethod
    def parse(cls, iterator) -> "Float64":
        return cls.build(iterator.get_float64())

    def dump(self, datagram) -> None:
        datagram.add_float64(self.__float__())

    @classmethod
    def dump_default(cls, datagram) -> None:
        datagram.add_float64(0.0)

    def _json(self) -> float:
        return self.__float__()


class String(ObjectBase, str):
    @classmethod
    def parse(cls, iterator) -> "String":
        return cls.build(iterator.get_string())

    def dump(self, datagram) -> None:
        datagram.add_string(self.__str__())

    @classmethod
    def dump_default(cls, datagram) -> None:
        datagram.add_string("")

    def _json(self) -> str:
        return self.__str__()


class MultilineString(String):
    @classmethod
    def parse(cls, iterator) -> "MultilineString":
        lines = iterator.get_uint8()
        value = "\n".join((iterator.get_string() for i in len(lines)))
        return cls.build(value)

    def dump(self, datagram) -> None:
        lines = self.__str__().splitlines()
        datagram.add_uint8(len(lines))
        for line in lines:
            datagram.add_string(line)

    @classmethod
    def dump_default(cls, datagram) -> None:
        datagram.add_uint8(0)


class DateTime(ObjectBase, datetime.datetime):
    FORMAT = "%H:%M:%S"

    @classmethod
    def parse(cls, iterator) -> "MultilineString":
        data = iterator.get_string()
        value = datetime.datetime.strptime(data, cls.FORMAT)
        return cls.build(value)

    def dump(self, datagram) -> None:
        value = self.strftime(self.FORMAT)
        datagram.add_string(value)

    @classmethod
    def dump_default(cls, datagram) -> None:
        datagram.add_string("")

    def _json(self) -> str:
        return self.strftime(self.FORMAT)
