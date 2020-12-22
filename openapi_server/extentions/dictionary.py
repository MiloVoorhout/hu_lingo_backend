"""
    This script is made to create new game libraries
"""
import re
import sys


def create_library(old_dictionary, new_dict_language):
    """
    Creates library in the filtered_dictionaries dict
    :return: nothing
    """
    with open('assets/unfiltered_dictionaries/' + old_dictionary + '.txt', 'r') as outfile:
        my_file = open('assets/filtered_dictionaries/' + new_dict_language.upper() + '.txt', 'w+')
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


if __name__ == '__main__':
    DICT_NAME = str(sys.argv[1])
    DICT_LANGUAGE = str(sys.argv[2])
    create_library(DICT_NAME, DICT_LANGUAGE)
