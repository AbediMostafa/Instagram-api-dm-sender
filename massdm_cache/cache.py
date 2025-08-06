from abc import ABC, abstractmethod
from typing import Any


class Cache(ABC):

    @classmethod
    async def create(cls, **kwargs):  # noqa
        raise NotImplementedError("Initiation logic must be implemented")

    @abstractmethod
    async def get(self, key):
        pass

    @abstractmethod
    async def set(self, key: Any, value: Any, ttl: None | int = None, appoximate: bool = True):
        pass

    @abstractmethod
    async def delete(self, key):
        pass

    @abstractmethod
    async def clear(self):
        pass

    @abstractmethod
    async def disconnect(self):
        pass