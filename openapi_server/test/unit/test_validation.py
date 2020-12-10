import unittest
from datetime import timedelta
from openapi_server.domain.game.validation import *


class TestValidation(unittest.TestCase):
    def test_word_validation(self):
        """Test word validation"""
        result = validate_word('nietbetaandwoord', 'NL')
        self.assertEqual(result, 'Given word does not exist')

    def test_alphabetic_validation(self):
        """Test alphabetic validation"""
        result = validate_only_alphabetic('éntre')
        self.assertEqual(result, 'Word contains punctuation marks')

    def test_length_validation(self):
        """Test word length validation"""
        result = validate_word_length('zeven', 7)
        self.assertEqual(result, 'Word is not the same length')

    def test_time_validation(self):
        """Test time validation"""
        start_time = datetime.now()
        now = (datetime.now() + timedelta(seconds=11)).strftime("%Y-%b-%d %H:%M:%S.%f")

        result = validate_time(start_time, now)
        self.assertEqual(result, 'Turn took longer than 10 seconds')


if __name__ == '__main__':
    unittest.main()
