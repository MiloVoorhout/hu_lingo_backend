"""
    This repository contains all functions for getting words
"""

import random


def get_random_word(word_length):
    """
    Get a random word from a filtered dictionary
    :param word_length: length of word that needs to be find
    :return: a random word with length x
    """
    random_word = ""

    with open('../assets/filtered_dictionaries/NL.txt', 'r') as words:
        filter_words = words.read().splitlines()
        while not len(random_word) == word_length:
            random_word = random.choice(filter_words).upper()

    return random_word
