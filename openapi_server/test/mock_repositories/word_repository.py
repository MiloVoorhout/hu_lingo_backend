"""
    This repository contains all functions for getting words
"""

import random

class TestWordRepository:
    """
    WordRepository class contains every word function that talks to the database
    """

    @staticmethod
    def get_random_word(word_length, language):
        """
        Get a random word from a filtered dictionary
        :param language: language of dictionary the word is from
        :param word_length: length of word that needs to be find
        :return: a random word with length x
        """
        random_word = ""
        filter_words = ['TESTS', 'BOOMER', 'ANDROID']

        while not len(random_word) == word_length:
            random_word = random.choice(filter_words).upper()

        return random_word
