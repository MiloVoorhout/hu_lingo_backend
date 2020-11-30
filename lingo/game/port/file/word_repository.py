import random


def get_random_word(word_length):
    random_word = ""

    with open('assets/filtered_dictionaries/NL.txt', 'r') as words:
        filter_words = words.read().splitlines()
        while not len(random_word) == word_length:
            random_word = random.choice(filter_words).upper()