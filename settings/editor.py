from settings.manager import ConfigManager


class ConfigEditor:
    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager

    def __enter__(self):
        self.edited_config = self.config_manager.get_config()
        return self.edited_config

    def __exit__(self, *args):
        self.config_manager.update_config(self.edited_config)
