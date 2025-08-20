from abc import ABC, abstractmethod
from typing import Any


class Cache(ABC):

    @classmethod
    def create(cls, **kwargs):  # noqa
        raise NotImplementedError("Initiation logic must be implemented")

    @abstractmethod
    def get(self, key) -> Any:
        pass

    @abstractmethod
    def set(self, key: Any, value: Any, ttl: None | int = None, appoximate: bool = True):
        pass

    @abstractmethod
    def delete(self, key):
        pass

    @abstractmethod
    def clear(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass