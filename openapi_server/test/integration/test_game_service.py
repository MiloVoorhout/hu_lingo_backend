import unittest
from openapi_server.core.application.game.game_logic import GameService
from openapi_server.test.mock_repositories.game_repository import TestGameRepository
from openapi_server.test.mock_repositories.round_repository import TestRoundRepository
from openapi_server.test.mock_repositories.turn_repository import TestTurnRepository
from openapi_server.test.mock_repositories.word_repository import TestWordRepository


class TestGameService(unittest.TestCase):
    game_service = GameService(game_repository=TestGameRepository(),
                               round_repository=TestRoundRepository(),
                               turn_repository=TestTurnRepository(TestRoundRepository()),
                               word_repository=TestWordRepository())

    # =========================
    # Test create game function
    # =========================
    def test_create_game_correct(self):
        response = self.game_service.create_game(1, 'NL')
        self.assertEqual(response[0], 'T')
        self.assertEqual(response[0].__eq__('B'), False)
        self.assertFalse(response[0].__eq__('A'), False)
        self.assertEqual(response[1], 5)
        self.assertEqual(response[1] == 6, False)
        self.assertEqual(response[1] == 7, False)

    def test_create_game_no_user(self):
        response = self.game_service.create_game(2, 'NL')
        self.assertEqual(response[0], 'T')

    # ================================
    # Test choose random word function
    # ================================
    def test_choose_random_word_len_5(self):
        response = self.game_service._choose_random_word(5, 'NL')
        self.assertEqual(len(response), 5)

    def test_choose_random_word_len_6(self):
        response = self.game_service._choose_random_word(6, 'NL')
        self.assertEqual(len(response), 6)

    def test_choose_random_word_len_7(self):
        response = self.game_service._choose_random_word(7, 'NL')
        self.assertEqual(len(response), 7)

    # ================================
    # Test guess turn function
    # ================================
    def test_guess_turn_correct_word(self):
        response = self.game_service.guess_turn(1, 'TESTS')
        self.assertEqual(response[0].__eq__('correct'), True)
        self.assertEqual(response[1].__eq__(
            ([
                 {'letter': 'T', 'letterFeedback': 'correct'},
                 {'letter': 'E', 'letterFeedback': 'correct'},
                 {'letter': 'S', 'letterFeedback': 'correct'},
                 {'letter': 'T', 'letterFeedback': 'correct'},
                 {'letter': 'S', 'letterFeedback': 'correct'}
             ])), True)

    def test_guess_turn_next_round(self):
        response = self.game_service.guess_turn(1, 'VETER')
        self.assertEqual(response[0].__eq__('next-round'), True)
        self.assertEqual(response[1].__eq__(
            ([
                 {'letter': 'V', 'letterFeedback': 'absent'},
                 {'letter': 'E', 'letterFeedback': 'correct'},
                 {'letter': 'T', 'letterFeedback': 'present'},
                 {'letter': 'E', 'letterFeedback': 'absent'},
                 {'letter': 'R', 'letterFeedback': 'absent'}
             ])), True)

    def test_guess_turn_validate_error(self):
        response = self.game_service.guess_turn(2, 'SDJBE5')
        self.assertEqual(response[0].__eq__('validation-error'), True)
        self.assertEqual(response[1].__eq__(
            ([
                 {'letter': 'S', 'letterFeedback': 'invalid'},
                 {'letter': 'D', 'letterFeedback': 'invalid'},
                 {'letter': 'J', 'letterFeedback': 'invalid'},
                 {'letter': 'B', 'letterFeedback': 'invalid'},
                 {'letter': 'E', 'letterFeedback': 'invalid'},
                 {'letter': '5', 'letterFeedback': 'invalid'}
             ])), True)
        self.assertEqual(response[2].__eq__(([
                 'Given word does not exist',
                 'Word contains punctuation marks',
                 'Word is not the same length',
                 'Turn took longer than 10 seconds'
             ])), True)

    def test_guess_turn_game_over(self):
        response = self.game_service.guess_turn(4, 'BETER')
        self.assertEqual(response[0].__eq__('game-over'), True)
        self.assertEqual(response[1].__eq__(
            ([
                 {'letter': 'B', 'letterFeedback': 'absent'},
                 {'letter': 'E', 'letterFeedback': 'correct'},
                 {'letter': 'T', 'letterFeedback': 'present'},
                 {'letter': 'E', 'letterFeedback': 'absent'},
                 {'letter': 'R', 'letterFeedback': 'absent'}
             ])), True)

    # =======================
    # Test change game status
    # =======================
    def test_change_game_status_length_5(self):
        response = self.game_service._change_game_status(5)
        self.assertTrue(response == 6)

    def test_change_game_status_length_6(self):
        response = self.game_service._change_game_status(6)
        self.assertTrue(response == 7)

    def test_change_game_status_length_7(self):
        response = self.game_service._change_game_status(7)
        self.assertTrue(response == 5)

    # =======================
    # Test change game status
    # =======================
    def test_create_round(self):
        response = self.game_service.create_round(1)
        self.assertTrue(len(response[0]), 5)
        self.assertTrue(response[1], 1)

    def test_create_round_no_round_id(self):
        response = self.game_service.create_round(5)
        self.assertEqual(response.__eq__('abort'), True)


if __name__ == '__main__':
    unittest.main()
