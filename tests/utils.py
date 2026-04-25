from zombie_nomnom import Die, DieBag, Face, ZombieDieGame
from zombie_nomnom_api.game import Game, InMemoryGameMaker


class FakeGameMaker(InMemoryGameMaker):

    def make_game(self, players: list[str]) -> Game:
        game = Game(game=ZombieDieGame(players, bag_function=self.winning_bag))
        self.session[game.id] = game
        return game

    def winning_bag(self):
        bag = DieBag(dice=[Die(faces=[Face.BRAIN] * 6) for _ in range(6)])
        return bag
