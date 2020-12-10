"""
    This script is made to create new game libraries
"""
import re


def create_library():
    """
    Creates library in the filtered_dictionaries dict
    :return: nothing
    """
    with open('assets/unfiltered_dictionaries/woorden.txt', 'r') as outfile:
        dict_language = "NL"
        my_file = open('assets/filtered_dictionaries/' + dict_language + '.txt', 'w+')
        for word in outfile:
            word = word.strip()
            if verify_word(word):
                my_file.write(word + "\n")

        my_file.close()


def verify_word(word):
    """
    Check if word is correct
    :param word: word that needs to be checked
    :return: a boolean of the check
    """
    return re.match('^[a-z]{5,7}$', word)