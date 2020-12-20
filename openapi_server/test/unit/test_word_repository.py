import unittest

from openapi_server.core.port.file.word_repository import WordRepository


class TestWordRepository(unittest.TestCase):
    # =================================
    # Test correct word length response
    # =================================
    def test_get_random_word_correct_length_5_characters(self):
        response = WordRepository().get_random_word(5, 'NL')
        self.assertTrue(len(response) == 5)

    def test_get_random_word_correct_length_6_characters(self):
        response = WordRepository().get_random_word(6, 'NL')
        self.assertTrue(len(response) == 6)

    def test_get_random_word_correct_length_7_characters(self):
        response = WordRepository().get_random_word(7, 'NL')
        self.assertTrue(len(response) == 7)

    # ==========================
    # Test wrong length response
    # ==========================
    def test_get_random_word_wrong_length(self):
        response = WordRepository().get_random_word(6, 'NL')
        self.assertFalse(len(response) == 5)


if __name__ == '__main__':
    unittest.main()
