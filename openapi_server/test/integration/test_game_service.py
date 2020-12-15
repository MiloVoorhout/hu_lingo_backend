import unittest

from openapi_server.core.application.game.game_logic import GameService
from openapi_server.core.port.data.game_repository import GameRepository
from openapi_server.core.port.data.round_repository import RoundRepository
from openapi_server.core.port.data.turn_repository import TurnRepository
from openapi_server.core.port.file.word_repository import WordRepository


class TestGameService(unittest.TestCase):
    round_repository = RoundRepository()
    game_service = GameService(game_repository=GameRepository(),
                               round_repository=round_repository,
                               turn_repository=TurnRepository(round_repository),
                               word_repository=WordRepository())

    def test_choose_random_word(self):
        response = self.game_service._choose_random_word(5, 'NL')
        self.assertEqual(len(response), 5)

    def test_change_game_status_length_5(self):
        response = self.game_service._change_game_status(5)
        self.assertTrue(response == 6)

    def test_change_game_status_length_6(self):
        response = self.game_service._change_game_status(6)
        self.assertTrue(response == 7)

    def test_change_game_status_length_7(self):
        response = self.game_service._change_game_status(7)
        self.assertTrue(response == 5)


if __name__ == '__main__':
    unittest.main()
