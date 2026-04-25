import uuid
import pytest

from pymongo import MongoClient
from pymongo.collection import Collection
from zombie_nomnom import ZombieDieGame
from zombie_nomnom.engine.serialization import format_to_json_dict

from zombie_nomnom_api.game import MongoGameMaker


@pytest.fixture(scope="session")
def mongo_client():
    return MongoClient("mongodb://localhost:27017/testing")


@pytest.fixture(scope="session")
def game_collection_name():
    return "games"


@pytest.fixture(scope="session")
def mongo_game_maker(mongo_client: MongoClient, game_collection_name: str):
    return MongoGameMaker(
        mongo_client=mongo_client,
        game_collection_name=game_collection_name,
    )


@pytest.fixture()
def game_collection(mongo_client: MongoClient, game_collection_name: str):
    game_coll = mongo_client.get_database().get_collection(game_collection_name)
    yield game_coll
    game_coll.drop()


@pytest.mark.mongo
def test_mongo_game_maker__when_making_a_game__saves_it_to_mongo(
    mongo_game_maker: MongoGameMaker,
    game_collection: Collection,
):
    mongo_game_maker.make_game(["player 1"])
    game_collection.find_one()


def create_game_dict(game: ZombieDieGame) -> dict:
    return {
        "id": str(uuid.uuid4()),
        "game": format_to_json_dict(game),
    }


def test_mongo_game_maker__when_iterating_over_games__loads_all_games_in_mango(
    mongo_game_maker: MongoGameMaker,
    game_collection: Collection,
):
    game_collection.insert_many(
        [
            create_game_dict(ZombieDieGame(["player 1"])),
            create_game_dict(ZombieDieGame(["player 2"])),
        ]
    )

    games = list(mongo_game_maker)

    assert len(games) == 2


def test_mongo_game_maker__when_iterating_over_empty_collection__returns_empty_list(
    mongo_game_maker: MongoGameMaker,
):
    # no seeded data.
    games = list(mongo_game_maker)

    assert len(games) == 0


def test_mongo_game_maker__when_getting_an_existing_game__returns_game(
    mongo_game_maker: MongoGameMaker,
    game_collection: Collection,
):
    instance = create_game_dict(ZombieDieGame(["player 1"]))
    game_collection.insert_one(instance)

    mango_instance = mongo_game_maker[instance["id"]]
    assert mango_instance is not None
    assert mango_instance.id == instance["id"]


def test_mongo_game_maker__when_getting_a_non_existent_game__returns_none(
    mongo_game_maker: MongoGameMaker,
):
    mango_instance = mongo_game_maker["dne"]
    assert mango_instance is None
