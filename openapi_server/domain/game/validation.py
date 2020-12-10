"""
    Validation domain where all validation analyses is done
"""
import os
import re
from datetime import datetime


def validate_word(guess, game_language):
    """
    Validates if the guess exists/has correct grammer
    :param game_language: Gets the right dictionary
    :param guess: String = users guessed word
    :return: Nothing
    """
    # Get absolute file path
    absolute_path = os.path.dirname(os.path.abspath(''))
    file_path = absolute_path + '/assets/filtered_dictionaries/' + game_language + '.txt'

    # Check if word exists / Check if right grammar
    with open(file_path, 'r') as dictionary:
        guess = guess.lower()
        if guess not in dictionary.read():
            return 'Given word does not exist'
    return ''


def validate_only_alphabetic(guess):
    """
    Check if all letters of the guess are alphabetic
    :param guess: String = users guessed word
    :return: Nothing
    """
    # Word only contains isalpha
    if not guess.isalpha():
        return 'Word contains punctuation marks'
    return ''


def validate_word_length(guess, word_length):
    """
    Checks if guess is as long as the correct word
    :param guess: String = users guessed word
    :param word_length: Correct word length
    :return: Nothing
    """
    # If word is right length
    if not len(guess) == word_length:
        return 'Word is not the same length'
    return ''


def validate_time(start_time, now):
    """
    Check if guess time is less or equal as 10
    :param start_time: Datetime = time of turn start
    :param now: Datetime = time of users guess
    :return: Nothing
    """
    # Make date time from NOW variable
    current_time = datetime.strptime(now, "%Y-%b-%d %H:%M:%S.%f")

    # Calculate the difference between date/times
    difference = current_time - start_time

    # Check if guess in 10 seconds
    # TODO: change time difference to 10 seconds
    if difference.seconds > 10000000:
        return 'Turn took longer than 10 seconds'
    return ''
