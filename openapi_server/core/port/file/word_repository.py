"""
    This repository contains all functions for getting words
"""

import random


# pylint: disable=too-few-public-methods
from pathlib import Path


class WordRepository:
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

        absolute_path = str(Path(__file__).parents[4])
        file_path = absolute_path + '/assets/filtered_dictionaries/' + language + '.txt'

        with open(file_path, 'r') as words:
            filter_words = words.read().splitlines()
            while not len(random_word) == word_length:
                random_word = random.choice(filter_words).upper()

        return random_word
