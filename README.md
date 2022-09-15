*Settings aims to provide a quick and easy way to manage your application's settings, while remaining flexible enough to allow your needs to evolve*

## Install

* By default, `settings` provides only a framework to manage settings using encoders / serializers. You can install `settings` without additional dependencies by running

```
pip install settings
```

* Most of the time you want to use one of the `defaults encoders/serializers`. In this case **you need to install its extra dependencies** using...

```
pip install settings[extra1, extra2]
```

...and replacing `extra1, extra2, ...` by the dependency you need.



### default encoders provided
| extra dependency |path                                       | description                                             |
| -|------------------------------------------ | ------------------------------------------------------- |
| pydantic-encoder | settings.encoders.pydantic.PydanticEncoder | Allow to have a pydantic BaseModel configuration object |


### default serializers provided
| extra dependency | path                                     | description                           |
|- |---------------------------------------- | ------------------------------------- |
| yaml-serializer |settings.serializers.yaml.YamlSerializer | Allow to save settings in yaml format |

## Quick start

We will start with a simple example using a pydantic basemodel as our config object and yaml formatting for our config file!

* First we install additional dependencies

```
pip install settings[pydantic-encoder,yaml-serializer]
```

* Then from our code, we instanciate our ConfigManager, passing it selected `encoder` and `serializer`.

```python
from settings.encoders.pydantic import PydanticEncoder
from settings.manager import ConfigManager
from settings.serializers.yaml import YamlSerializer

config_manager = ConfigManager(
    # used to let user provide alternative config path through an environment variable
    envvar="MYAPP_CONFIG",
    # used tas fallback config path if variable is not set
    default_path=config_file,
    encoder=PydanticEncoder(MyConfigClass),
    serializer=YamlSerializer()
)
```

* Then we need to define our config object required to instanciate `PydanticEncoder`. Obviously this step is specific to `PydanticEncoder`.

```python
from datetime import datetime
from pydantic import BaseModel, Field

class MySubconfig(BaseModel):
    setting_a: str = "default"
    setting_b: int = 0
    setting_c: datetime = Field(default_factory=datetime.utcnow)

class MyConfigClass(BaseModel):
    sub_config: MySubconfig = Field(default_factory=MySubconfig)
```

Once done you can simply get config using the following snippet. It config file does not exists yet, it is initialized automatically given that your pydantic model has default values for all of its fields.

```python
my_config = config_manager.get_config()
print(my_config.sub_config.setting_c)
```

If you want to edit the config from your code, you just have to

```python
with config_manager.get_edit_context() as config:
    config.sub_config.setting_a = "new-value"
```

## Advanced usage

Sometimes you wont find encoders/serializers that suit your needs in `settings` package... Don't be sad, you can create your own, then pass it to the ConfigManager exactly the same way internal encoders/serializers works! Keep reading for implementation details...

### Custom encoders

```python
from typing import TypeVar, Union
from settings.encoders.base import ConfigEncoder

# your config type
T = TypeVar("T")


class ExampleEncoder(ConfigEncoder[MyConfigClass]):
    def encode(self, config_obj: MyConfigClass) -> Union[dict, list]:
        # takes your config object, and returns a serializable object

    def decode(self, config_data: Union[dict, list]) -> MyConfigClass:
        # takes a serializable object and returns your config object

    def default(self) -> MyConfigClass:
        # returns default value when config does not exists

```

### Custom decoders

```python
from io import TextIOWrapper
from typing import Union

import yaml

from settings.serializers.base import ConfigSerializer


class ExampleSerializer(ConfigSerializer):
    def serialize(self, config_data: Union[dict, list], file: TextIOWrapper):
        # takes serializable data and write it to config file

    def deserialize(self, file: TextIOWrapper) -> Union[dict, list]:
        # parse config file and returns serializable data
```

### Use custom encoders/decoders

```python
config_manager = ConfigManager(
    # used to let user provide alternative config path through an environment variable
    envvar="MYAPP_CONFIG",
    # used tas fallback config path if variable is not set
    default_path=config_file,
    encoder=ExampleEncoder(),
    serializer=ExampleSerializer()
)
```

...exactly the same way internal encoders/serializers works!

## Contribute

To be continued...
