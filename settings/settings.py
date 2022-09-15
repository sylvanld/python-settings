import os


def get_config_path(envvar: str = None, default_path: str = None):
    value = None

    if envvar is None and default_path is None:
        raise ValueError(
            "You must specify at least one of envvar or default path to provide configuration file path."
        )

    if envvar is not None:
        value = os.getenv(envvar)

    if value is None:
        if default_path is None:
            raise FileNotFoundError(
                f"You must set environment variable '{envvar}' to indicate config file location."
            )
        else:
            value = default_path

    return os.path.abspath(os.path.expanduser(value))
