"""
    This script is made to create new game libraries
"""


def create_library():
    """
    Creates library in the filtered_dictionaries dict
    :return: nothing
    """
    with open('../../assets/unfiltered_dictionaries/woorden.txt', 'r') as outfile:
        dict_language = "NL"
        my_file = open('../../assets/filtered_dictionaries/' + dict_language + '.txt', 'w+')
        for word in outfile:
            word = word.strip()
            if not word[0].isupper():
                if 5 <= len(word) <= 7 and word.isalpha():
                    my_file.write(word + "\n")

        my_file.close()
