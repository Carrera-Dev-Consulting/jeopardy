from fastapi.testclient import TestClient

from zombie_nomnom import Command, Die, Face, RoundState
from zombie_nomnom.engine import DrawDice, Score

from zombie_nomnom_api.game import GameMakerInterface
from zombie_nomnom_api.graphql_app.dependencies import DIContainer

from tests.integration.zombie_nomnom_api.graphql.util import query_api


def winning_die():
    return Die(current_face=Face.BRAIN, faces=[Face.BRAIN] * 6)


class Win(Command):
    def execute(self, round: RoundState):
        return RoundState(
            player=round.player.add_dice(
                *(winning_die() for _ in range(20))
            ).calculate_score(),
            bag=round.bag.model_copy(),
            ended=True,
        )


def test_query_games__when_queried__returns_games_as_expected(
    di_container: DIContainer,
    api_client: TestClient,
):
    maker: GameMakerInterface = di_container[GameMakerInterface]
    existing_game = maker.make_game(["player1", "player2"])
    existing_game.game.process_command(DrawDice(3))
    existing_game.game.process_command(Win())
    existing_game.game.process_command(Score())
    maker.make_game(["player3", "player4"])
    query = """
    query GetAllGames {
        games {
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
                score
                hand {
                    color
                    currentFace
                }
            }
            round {
                player {
                    id
                }
                bag {
                    dice {
                        color
                        currentFace
                        sides
                    }
                    drawnDice {
                        color
                        currentFace
                    }
                }
                points
                ended
            }
            gameOver
            winner {
                id
                name
            }
        }
    }
    """

    response = query_api(api_client, query)
    assert response.status_code == 200, "Expected 200 OK"
    value = response.json()["data"]["games"]
    assert len(value) == 2, "Expected 2 games"
    game = value[0]
    assert game["id"] == existing_game.id, "Expected first game to be the existing game"
    assert len(game["moves"]) == 3, "Expected first game to have 3 moves"
