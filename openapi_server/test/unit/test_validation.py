import unittest
from datetime import timedelta, datetime

from openapi_server.core.domain.game.validation import validate_word, validate_only_alphabetic, validate_word_length, \
    validate_time


class TestValidation(unittest.TestCase):
    def test_word_validation_word_does_not_exist(self):
        """Test word validation"""
        result = validate_word('nietbetaandwoord', 'NL')
        self.assertEqual(result, 'Given word does not exist')

    def test_word_validation_word_does_exist(self):
        """Test word validation"""
        result = validate_word('baard', 'NL')
        self.assertEqual(result, '')

    def test_alphabetic_validation_word_contains_non_alphabetic_characters(self):
        """Test alphabetic validation"""
        result = validate_only_alphabetic('entre0')
        self.assertEqual(result, 'Word contains punctuation marks')

    def test_alphabetic_validation_word_only_contains_alphabetic_characters(self):
        """Test alphabetic validation"""
        result = validate_only_alphabetic('check')
        self.assertEqual(result, '')

    def test_length_validation_not_correct_length(self):
        """Test word length validation"""
        result = validate_word_length('zeven', 7)
        self.assertEqual(result, 'Word is not the same length')

    def test_length_validation_correct_length(self):
        """Test word length validation"""
        result = validate_word_length('woord', 5)
        self.assertEqual(result, '')

    def test_time_validation_turn_took_to_long(self):
        """Test time validation"""
        start_time = datetime.now()
        now = (datetime.now() + timedelta(seconds=11)).strftime("%Y-%b-%d %H:%M:%S.%f")

        result = validate_time(start_time, now)
        self.assertEqual(result, 'Turn took longer than 10 seconds')

    def test_time_validation_turn_took_exactly_10_seconds(self):
        """Test time validation"""
        start_time = datetime.now()
        now = (datetime.now() + timedelta(seconds=10)).strftime("%Y-%b-%d %H:%M:%S.%f")

        result = validate_time(start_time, now)
        self.assertEqual(result, '')

    def test_time_validation_turn_took_under_10_seconds(self):
        """Test time validation"""
        start_time = datetime.now()
        now = (datetime.now() + timedelta(seconds=10)).strftime("%Y-%b-%d %H:%M:%S.%f")

        result = validate_time(start_time, now)
        self.assertEqual(result, '')


if __name__ == '__main__':
    unittest.main()
