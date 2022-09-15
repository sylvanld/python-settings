import datetime
import os
from typing import List

from pydantic import BaseModel, Field

from settings.encoders.pydantic import PydanticEncoder
from settings.manager import ConfigManager
from settings.serializers.yaml import YamlSerializer


# defines config class
class DailyConfig(BaseModel):
    members: List[str] = Field(default_factory=list)
    time: datetime.time = Field(default_factory=lambda: datetime.time(hour=8))


class AppConfig(BaseModel):
    daily: DailyConfig = Field(default_factory=DailyConfig)


def test_simple():
    config_file = "here.yaml"

    # ensure no config file exists prior to the test
    try:
        os.remove(config_file)
    except FileNotFoundError:
        ...

    # instanciate config class
    config_manager = ConfigManager(
        default_path=config_file,
        encoder=PydanticEncoder(AppConfig),
        serializer=YamlSerializer(),
    )

    # check that initially config is the default config
    config = config_manager.get_config()
    assert len(config.daily.members) == 0
    assert config.daily.time.hour == 8

    # edit configuration file using edit context
    with config_manager.get_edit_context() as config:
        config.daily.time = datetime.time(hour=9, minute=30)
        config.daily.members.append("daria")
        config.daily.members.append("romain")

    # check that config has been edited correctly
    config = config_manager.get_config()
    assert len(config.daily.members) == 2
    assert config.daily.time.hour == 9
    assert config.daily.time.minute == 30


if __name__ == "__main__":
    test_simple()
