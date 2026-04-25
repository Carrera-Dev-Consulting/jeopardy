from tests.integration.zombie_nomnom_api.graphql.util import query_api
from tests.utils import FakeGameMaker
from zombie_nomnom_api.game import InMemoryGameMaker, GameMakerInterface
from zombie_nomnom.engine import DrawDice


def test_mutation_create_game__when_making_a_game__creates_a_game_with_maker(
    di_container,
    api_client,
):
    maker: GameMakerInterface = di_container[GameMakerInterface]
    original_value = len(list(maker))
    mutation_query = """
    mutation MakeAGame($players: [String!]!){
        createGame(players: $players) {
            errors
            game {
                id
                moves {
                    name
                    player {
                        id
                        name
                    }
                }
                players {
                    id
                    name
                }
            }
        }
    }
    """
    reponse = query_api(
        api_client,
        query=mutation_query,
        variables={"players": ["player one", "player two"]},
    )

    assert reponse.status_code == 200
    assert len(list(maker)) == original_value + 1
    value = reponse.json()["data"]["createGame"]
    assert value["errors"] == []
    assert maker[value["game"]["id"]] is not None


def test_mutation_draw_dice_with_a_fresh_game(di_container, api_client):
    di_container[GameMakerInterface] = FakeGameMaker()
    maker: InMemoryGameMaker = di_container[GameMakerInterface]
    existing_game = maker.make_game(["player1"])
    original_hand = existing_game.game.round.player.hand
    original_bag_size = len(existing_game.game.round.bag)
    mutation_query = """
    mutation DrawDice($gameId: ID!) {
        drawDice(gameId: $gameId) {
            errors
            round {
                player {
                    hand {
                        currentFace
                    }
                }
            }
        }
    }
    """
    response = query_api(
        api_client,
        query=mutation_query,
        variables={"gameId": existing_game.id},
    )
    existing_game = maker[existing_game.id]
    assert response.status_code == 200
    assert len(response.json()["data"]["drawDice"]["errors"]) == 0
    assert len(original_hand) == 0
    assert len(existing_game.game.round.player.hand) == 3
    assert len(existing_game.game.round.bag) == (original_bag_size - 3)


def test_mutation_score_with_three_brains_after_drawing(di_container, api_client):
    di_container[GameMakerInterface] = FakeGameMaker()
    maker: GameMakerInterface = di_container[GameMakerInterface]
    existing_game = maker.make_game(["player1", "player2"])

    existing_game.game.process_command(DrawDice())
    mutation_query = """
    mutation EndRound($gameId: ID!){
        endRound(gameId: $gameId){
            errors
            round{
                player{
                    score
                }
                ended
            }
        }
    }
    """
    response = query_api(
        api_client,
        query=mutation_query,
        variables={"gameId": existing_game.id},
    )
    existing_game = maker[existing_game.id]
    current_player = existing_game.game.round.player
    assert response.status_code == 200
    end_round_json = response.json()["data"]["endRound"]
    assert len(end_round_json["errors"]) == 0
    assert existing_game.game.players[0].total_brains == 3
    assert current_player.name == "player2"
    assert end_round_json["round"]["ended"]
