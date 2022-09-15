import logging
from typing import ContextManager, Generic, TypeVar

from settings.encoders.base import ConfigEncoder
from settings.serializers.base import ConfigSerializer
from settings.settings import get_config_path

T = TypeVar("T")


class ConfigManager(Generic[T]):
    def __init__(
        self,
        *,
        encoder: ConfigEncoder[T],
        serializer: ConfigSerializer,
        envvar: str = None,
        default_path: str = None,
        autoinit: bool = True
    ):
        self.logger = logging.getLogger(__name__)
        self.path = get_config_path(envvar, default_path)
        self.encoder = encoder
        self.serializer = serializer
        self.autoinit = autoinit

    def __unsafe_get_config(self) -> T:
        self.logger.debug("opening config from: %s", self.path)
        with open(self.path, "r", encoding="utf-8") as config_file:
            raw_config = self.serializer.deserialize(config_file)

        return self.encoder.decode(raw_config)

    def get_default_config(self):
        return self.encoder.default()

    def get_config(self) -> T:
        try:
            config = self.__unsafe_get_config()
        except FileNotFoundError as error:
            if not self.autoinit:
                self.logger.error("Configuration file not found in: %s", self.path)
                raise FileNotFoundError(
                    "Configuration file not found in: %s" % self.path
                ) from error
            self.logger.info("Initializing config to default in: %s", self.path)
            config = self.get_default_config()
            self.update_config(config)
        return config

    def update_config(self, config_obj: T):
        serializable_config = self.encoder.encode(config_obj)

        with open(self.path, "w", encoding="utf-8") as config_file:
            self.logger.debug("Saving config in: %s", self.path)
            self.serializer.serialize(serializable_config, config_file)

    def get_edit_context(self) -> ContextManager[T]:
        from settings.editor import ConfigEditor

        return ConfigEditor(self)
