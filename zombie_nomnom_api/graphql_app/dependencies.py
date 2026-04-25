from functools import cache
from typing import Any

from zombie_nomnom_api import configs
from zombie_nomnom_api.game import GameMakerInterface, create_maker
from zombie_nomnom.engine import DrawDice, Score

_unset = object()


class DIContainer:
    def __init__(self) -> None:
        self._dependencies = {}

    def __getitem__(self, key: Any) -> Any:
        value = self.get(key, _unset)
        if value is _unset:
            raise KeyError(key)
        return value

    def __setitem__(self, key: Any, value: Any) -> None:
        self.register(key, value)

    def register(self, key: type | str, value: Any = None) -> None:
        if isinstance(key, str) and not value:
            raise ValueError("value must be provided if key is a string")
        self._dependencies[str(key)] = value or key

    def get(self, key: Any, default: Any = None) -> Any:
        value = self._dependencies.get(str(key), default)
        if isinstance(value, type):
            # TODO(Milo): Handle dependency injection for anything the constructor needs.
            value = self._dependencies[str(key)] = value()
        return value


@cache
def bootstrap() -> DIContainer:
    container = DIContainer()
    container[GameMakerInterface] = create_maker(configs.game_maker_type)
    container[DrawDice] = DrawDice()
    container[Score] = Score()
    return container
