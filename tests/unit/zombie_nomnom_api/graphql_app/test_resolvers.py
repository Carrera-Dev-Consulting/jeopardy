import pytest
from zombie_nomnom import Die, DieBag, DieColor, Face, ZombieDieGame
from tests.utils import FakeGameMaker
from zombie_nomnom_api.game import Game, InMemoryGameMaker, GameMakerInterface
from zombie_nomnom.engine import DrawDice, Score
from zombie_nomnom_api.graphql_app.dependencies import DIContainer
from zombie_nomnom_api.graphql_app.resolvers import (
    die_color_resolver,
    games_resolver,
    create_game_resolver,
    draw_dice_resolver,
    end_round_resolver,
)


@pytest.fixture
def di_container() -> DIContainer:
    container = DIContainer()
    container[DrawDice] = DrawDice()
    container[Score] = Score()
    return container


@pytest.fixture
def game_maker():
    return InMemoryGameMaker()


def test_end_round_resolver_when_game_does_not_exist_returns_error(
    di_container: DIContainer,
    game_maker: InMemoryGameMaker,
):
    di_container[GameMakerInterface] = game_maker
    gameId = None
    round = end_round_resolver(None, None, gameId=gameId, dependencies=di_container)
    assert len(round["errors"]) == 1
    assert "No game id provided" in round["errors"][0]


def test_end_round_resolver_when_game_is_not_found_returns_error(
    di_container: DIContainer,
    game_maker: InMemoryGameMaker,
):
    di_container[GameMakerInterface] = game_maker
    gameId = "None"
    round = end_round_resolver(None, None, gameId=gameId, dependencies=di_container)
    assert len(round["errors"]) == 1
    assert f"Game id not found: {gameId}" in round["errors"][0]


def test_end_round_resolver_ends_round_and_scores_the_user(di_container: DIContainer):
    di_container[GameMakerInterface] = FakeGameMaker()
    game_maker: InMemoryGameMaker = di_container[GameMakerInterface]
    game = game_maker.make_game(["player1"])

    draw_dice_resolver(None, None, gameId=game.id, dependencies=di_container)
    round = end_round_resolver(None, None, gameId=game.id, dependencies=di_container)

    assert len(round["errors"]) == 0
    assert round["round"] is not None
    assert round["round"].ended
    assert round["round"].player.total_brains == 3


def test_draw_dice_resolver_draws_new_hand_when_draw_is_called(
    di_container: DIContainer,
):
    di_container[GameMakerInterface] = FakeGameMaker()
    game_maker: GameMakerInterface = di_container[GameMakerInterface]

    game = game_maker.make_game(["player1"])
    round = draw_dice_resolver(None, None, gameId=game.id, dependencies=di_container)

    assert len(round["errors"]) == 0
    assert round["round"] is not None


def test_draw_dice_resolver_when_game_does_not_exist_returns_error(
    di_container: DIContainer,
    game_maker: InMemoryGameMaker,
):
    di_container[GameMakerInterface] = game_maker
    gameId = None
    round = draw_dice_resolver(None, None, gameId=gameId, dependencies=di_container)
    assert len(round["errors"]) == 1
    assert "No game id provided" in round["errors"][0]


def test_draw_dice_resolver_when_game_is_not_found_returns_error(
    di_container: DIContainer,
    game_maker: InMemoryGameMaker,
):
    di_container[GameMakerInterface] = game_maker
    gameId = "None"
    round = draw_dice_resolver(None, None, gameId=gameId, dependencies=di_container)
    assert len(round["errors"]) == 1
    assert f"Game id not found: {gameId}" in round["errors"][0]


def test_games_resolver__when_given_an_id_and_game_exists__returns_list_with_game(
    di_container: DIContainer,
    game_maker: InMemoryGameMaker,
):
    di_container[GameMakerInterface] = game_maker
    game = game_maker.make_game(["player1", "player2"])
    games = games_resolver(None, None, id=game.id, dependencies=di_container)
    assert len(games) == 1
    assert games[0] == game


def test_games_resolver__when_given_an_id_and_game_does_not_exist__returns_empty_list(
    di_container: DIContainer,
    game_maker: InMemoryGameMaker,
):
    di_container[GameMakerInterface] = game_maker
    games = games_resolver(
        None, None, id="This game is on fire!!", dependencies=di_container
    )
    assert len(games) == 0


def test_games_resolver__when_not_given_an_id__returns_all_games(
    di_container: DIContainer,
    game_maker: InMemoryGameMaker,
):
    di_container[GameMakerInterface] = game_maker
    game_maker.make_game(["player1", "player2"])
    game_maker.make_game(["player3", "player4"])

    games = games_resolver(None, None, dependencies=di_container)
    assert len(games) == 2


def test_create_game_resolver__when_no_players_provided__returns_error(
    di_container: DIContainer,
    game_maker: InMemoryGameMaker,
):
    di_container[GameMakerInterface] = game_maker
    response = create_game_resolver(None, None, players=[], dependencies=di_container)

    assert response["errors"]
    assert response["game"] is None

    assert len(list(game_maker)) == 0


def test_create_game_resolver__when_players_provided__returns_new_game_instance(
    di_container: DIContainer,
    game_maker: InMemoryGameMaker,
):
    di_container[GameMakerInterface] = game_maker
    response = create_game_resolver(
        None, None, players=["Player One"], dependencies=di_container
    )

    assert response["errors"] == []
    assert response["game"]

    assert len(list(game_maker)) == 1


def test_die_color_resolver_returns_green_die_for_three_brains():
    die = die_color_resolver(Die(faces=[Face.BRAIN] * 6), None)
    assert die == DieColor.GREEN


def test_die_color_resolver_returns_yellow_die_for_two_brains():
    die = die_color_resolver(Die(faces=[Face.BRAIN] * 2 + [Face.FOOT] * 4), None)
    assert die == DieColor.YELLOW


def test_die_color_resolver_returns_red_die_for_one_brain():
    die = die_color_resolver(Die(faces=[Face.BRAIN] + [Face.FOOT] * 5), None)
    assert die == DieColor.RED
