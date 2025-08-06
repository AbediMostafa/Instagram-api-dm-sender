from abc import ABC, abstractmethod


class Cache(ABC):

    @classmethod
    async def create(cls, **kwargs):
        raise NotImplemented

    @abstractmethod
    async def get(self, key):
        pass

    @abstractmethod
    async def set(self, key, value, ttl=None):
        pass

    @abstractmethod
    async def delete(self, key):
        pass

    @abstractmethod
    async def clear(self):
        pass
