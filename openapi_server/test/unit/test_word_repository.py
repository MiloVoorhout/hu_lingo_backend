import unittest

from openapi_server.core.port.file.word_repository import WordRepository


class TestWordRepository(unittest.TestCase):

    def test_get_random_word_correct_length(self):
        response = WordRepository().get_random_word(5, 'NL')
        self.assertTrue(len(response) == 5)

    def test_get_random_word_wrong_length(self):
        response = WordRepository().get_random_word(6, 'NL')
        self.assertFalse(len(response) == 5)


if __name__ == '__main__':
    unittest.main()
