from abc import ABC, abstractmethod
import random
import time
from typing import Any, ClassVar, Generic, Type, TypeVar

from db.models import Account
from instagram_api_wrapper.client import InstagramAPIWrapper
from settings import Sleep

O = TypeVar("O")


class AbstractWorkflow(ABC, Generic[O]):
    """
    Workflow object is a callable that has a set of tasks and a set of dependencies.
    On calling a Workflow first the dependencies are executed and then the tasks.
    """

    tasks: ClassVar[list[Type["AbstractWorkflow"]]] = []
    dependencies: ClassVar[list[Type["AbstractWorkflow"]]] = []
    _store: dict

    def __init__(self, *args, **kwargs: Any) -> None:
        self.args = args
        self.kwargs = kwargs
        self._store = dict()

    @abstractmethod
    def execute(self, *args, **kwargs) -> O:
        pass

    def __call__(self) -> O:
        result = None
        if self.dependencies:
            first_d = self.dependencies.pop()
            result = first_d()
            for D in self.dependencies:
                result = D(result)()

        for T in self.tasks:
            result = T(result)()
        return self.execute(*self.args, **self.kwargs)


class InstagramWorkflow(AbstractWorkflow[InstagramAPIWrapper]):
    def __init__(self, *args, **kwargs: Any) -> None:
        api = kwargs.get("api")
        if not api or not isinstance(api, InstagramAPIWrapper):
            raise ValueError(
                f"{type(self)} objects need keyword argument `api` of \
                    type InstagramAPIWrapper on initializing"
            )
        self.kwargs = kwargs
        self.args = args


class Login(InstagramWorkflow):
    def execute(
        self, *, api: InstagramAPIWrapper, account: Account, **kwargs
    ) -> InstagramAPIWrapper:
        time.sleep(random.uniform(*Sleep.before_login))
        api.login_scenario()
        return api


# class SendDm(InstagramWorkflow):
#     dependencies = [Login]

#     def execute(
#         self, api: InstagramAPIWrapper, account: Account, **kwargs
#     ) -> InstagramAPIWrapper:
#         api.login_scenario()
#         return api
