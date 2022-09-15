from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Union

T = TypeVar("T")


class ConfigEncoder(ABC, Generic[T]):
    @abstractmethod
    def encode(self, config_obj: T) -> Union[dict, list]:
        raise NotImplementedError

    @abstractmethod
    def decode(self, config_data: Union[dict, list]) -> T:
        raise NotImplementedError

    @abstractmethod
    def default(self):
        raise NotImplementedError
