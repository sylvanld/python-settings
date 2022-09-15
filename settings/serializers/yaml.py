from io import TextIOWrapper
from typing import Union

import yaml

from settings.serializers.base import ConfigSerializer


class YamlSerializer(ConfigSerializer):
    def serialize(self, config_data: Union[dict, list], file: TextIOWrapper):
        return yaml.safe_dump(config_data, file)

    def deserialize(self, file: TextIOWrapper) -> Union[dict, list]:
        return yaml.safe_load(file)
