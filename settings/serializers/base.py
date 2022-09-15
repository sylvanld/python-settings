from abc import ABC, abstractmethod
from io import TextIOWrapper
from typing import Union


class ConfigSerializer(ABC):
    @abstractmethod
    def deserialize(self, file: TextIOWrapper) -> Union[dict, list]:
        raise NotImplementedError

    @abstractmethod
    def serialize(self, config_data: Union[dict, list], file: TextIOWrapper):
        raise NotImplementedError
