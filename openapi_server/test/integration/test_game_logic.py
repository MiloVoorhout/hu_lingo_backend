from datetime import timedelta, datetime
import unittest

from openapi_server.core.domain.game.game import run_turn


class TestGameLogicIntegration(unittest.TestCase):
    # ======================
    # Test run_turn function
    # ======================
    def test_run_turn_correct_word(self):
        """Test if run_turn gives correct response after running al functions"""
        response = run_turn(
            'PIZZA',
            'PIZZA',
            5,
            datetime.now(),
            (datetime.now() + timedelta(seconds=10)),
            2,
            'NL')
        self.assertEqual(response.__eq__(
            ('correct',
             [
                 {'letter': 'P', 'letterFeedback': 'correct'},
                 {'letter': 'I', 'letterFeedback': 'correct'},
                 {'letter': 'Z', 'letterFeedback': 'correct'},
                 {'letter': 'Z', 'letterFeedback': 'correct'},
                 {'letter': 'A', 'letterFeedback': 'correct'}
             ],
             '')), True)

    def test_run_turn_normal_guess(self):
        """Test if run_turn gives correct response after running al functions"""
        response = run_turn(
            'DRAAD',
            'BAARD',
            5,
            datetime.now(),
            (datetime.now() + timedelta(seconds=10)),
            2,
            'NL')
        self.assertEqual(response.__eq__(
            ('next-round',
             [
                 {'letter': 'D', 'letterFeedback': 'absent'},
                 {'letter': 'R', 'letterFeedback': 'present'},
                 {'letter': 'A', 'letterFeedback': 'correct'},
                 {'letter': 'A', 'letterFeedback': 'present'},
                 {'letter': 'D', 'letterFeedback': 'correct'}
             ],
             '')), True)

    def test_run_turn_game_over(self):
        """Test if run_turn gives correct response after running al functions"""
        response = run_turn(
            'DRAAD',
            'BAARD',
            5,
            datetime.now(),
            (datetime.now() + timedelta(seconds=10)),
            5,
            'NL')
        self.assertEqual(response.__eq__(
            ('game-over',
             [
                 {'letter': 'D', 'letterFeedback': 'absent'},
                 {'letter': 'R', 'letterFeedback': 'present'},
                 {'letter': 'A', 'letterFeedback': 'correct'},
                 {'letter': 'A', 'letterFeedback': 'present'},
                 {'letter': 'D', 'letterFeedback': 'correct'}
             ],
             '')), True)

    def test_run_turn_validation_error_all_validations(self):
        """Test if run_turn gives correct response after running al functions"""
        response = run_turn(
            'PIZZANA5',
            'PIZZA',
            5,
            datetime.now(),
            (datetime.now() + timedelta(seconds=11)),
            2,
            'NL')
        self.assertEqual(response.__eq__(
            ('validation-error',
             [
                 {'letter': 'P', 'letterFeedback': 'invalid'},
                 {'letter': 'I', 'letterFeedback': 'invalid'},
                 {'letter': 'Z', 'letterFeedback': 'invalid'},
                 {'letter': 'Z', 'letterFeedback': 'invalid'},
                 {'letter': 'A', 'letterFeedback': 'invalid'},
                 {'letter': 'N', 'letterFeedback': 'invalid'},
                 {'letter': 'A', 'letterFeedback': 'invalid'},
                 {'letter': '5', 'letterFeedback': 'invalid'}
             ],
             [
                 'Given word does not exist',
                 'Word contains punctuation marks',
                 'Word is not the same length',
                 'Turn took longer than 10 seconds'
             ])), True)


if __name__ == '__main__':
    unittest.main()
