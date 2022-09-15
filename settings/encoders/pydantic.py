import json
from typing import Type, TypeVar, Union

from pydantic import BaseModel
from pydantic.json import pydantic_encoder

from settings.encoders.base import ConfigEncoder

T = TypeVar("T", bound=BaseModel)


class PydanticEncoder(ConfigEncoder[T]):
    def __init__(self, base_model: Type[T]):
        self.base_model = base_model

    def encode(self, config_obj: T) -> Union[dict, list]:
        return json.loads(json.dumps(config_obj, default=pydantic_encoder))

    def decode(self, config_data: Union[dict, list]) -> T:
        return self.base_model.parse_obj(config_data)

    def default(self):
        return self.base_model()
