from enum import Enum
from typing import Protocol, runtime_checkable
import uuid

from pydantic_settings import BaseSettings
from pymongo.collection import Collection
from pymongo import MongoClient

from zombie_nomnom import ZombieDieGame
from zombie_nomnom.engine.serialization import format_to_json_dict, parse_game_json_dict


class Game:
    game: ZombieDieGame
    id: str

    def __init__(self, *, game: ZombieDieGame, id: str = None) -> None:
        self.game = game
        self.id = id or str(uuid.uuid4())

    def __eq__(self, value: object) -> bool:
        return isinstance(value, Game) and self.id == value.id

    @classmethod
    def from_dict(cls, game_data: dict) -> "Game":
        id = game_data.pop("id", None)
        game = parse_game_json_dict(game_data["game"])
        return cls(game=game, id=id)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "game": format_to_json_dict(self.game),
        }


@runtime_checkable
class GameMakerInterface(Protocol):
    """
    Defines the methods that are used by game makers to create and load games currently.
    """

    def make_game(self, players: list[str]) -> Game: ...

    def __getitem__(self, key: str) -> Game: ...

    def __iter__(self): ...


class InMemoryGameMaker:
    def __init__(self) -> None:
        self.session = {}

    def make_game(self, players: list[str]) -> Game:
        game = Game(game=ZombieDieGame(players))
        self.session[game.id] = game
        return game

    def __getitem__(self, key: str) -> Game:
        return self.session.get(key, None)

    def __iter__(self):
        return iter(self.session.values())


class MongoGameMaker:
    def __init__(self, mongo_client: MongoClient, game_collection_name) -> None:
        self.mongo_client = mongo_client
        self.game_collection: Collection = mongo_client.get_database().get_collection(
            game_collection_name
        )

    def make_game(self, players: list[str]) -> Game:
        game = Game(game=ZombieDieGame(players))
        self.game_collection.insert_one(game.to_dict())
        return game

    def load_game(self, game_id: str) -> Game | None:
        game_data = self.game_collection.find_one({"id": game_id})
        if game_data is None:
            return None

        game = Game.from_dict(game_data)
        return game

    def get_all_games(self) -> list[Game]:
        games_data = self.game_collection.find()
        games = [Game.from_dict(game_data) for game_data in games_data]
        return games

    def __getitem__(self, key: str) -> Game:
        return self.load_game(key)

    def __iter__(self):
        return iter(self.get_all_games())


class MongoGameMakerConfig(BaseSettings):
    """Environment Config settings for MongoGameMakers to allow us to not have to
    need mongo connection details unless we are loading the mongo engine.
    """

    mongo_connection: str = "mongodb://localhost:27017/zombie_nomnom"
    """
    Full mongo connection string uri ex. mongodb://localhost:27017/zombie_nomnom
    """
    game_collection_name: str = "games"
    """
    Name of the collection where we store game data.
    """


class GameMakerType(str, Enum):
    """
    Enum for the supported types of game makers we have implemented.
    """

    memory = "memory"
    mongo = "mongo"


def create_maker(kind: GameMakerType) -> GameMakerInterface:
    """Translates the game maker type to the implementation of the GameMakerInterface

    **Parameters**
    - kind (GameMakerType): The kind of game maker we want.

    **Raises**
    - ValueError: Given a GameMakerType that we do not have mapped.

    **Returns**
    - GameMakerInterface: GameMaker implementation
    """
    if kind == GameMakerType.mongo:
        config = MongoGameMakerConfig()
        return MongoGameMaker(
            game_collection_name=config.game_collection_name,
            mongo_client=MongoClient(config.mongo_connection),
        )
    elif kind == GameMakerType.memory:
        return InMemoryGameMaker()
    raise ValueError(f"Invalid game maker type: {kind}")
