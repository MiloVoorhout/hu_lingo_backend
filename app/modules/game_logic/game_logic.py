import random

word_length = 0
correct_word = ""


def choose_random_word(length):
    # TODO: Add logic where you find a random word based on length of current round and language

    with open('assets/filtered_dictionaries/NL.txt', 'r') as words:
        something = words.read().splitlines()
        global correct_word, word_length
        correct_word = random.choice(something).upper()
        word_length = len(correct_word)


def guess_turn(guess, time):
    validate_word_length(guess)
    validate_only_alphabetic(guess)
    validate_time(time)

    # Change word to lower
    guess = guess.lower()
    validate_word(guess)

    # If everything is correct do the following:
    # Change word to CAPS
    guess = guess.upper()
    word_response = []
    for iteration, char in enumerate(guess):
        if char in correct_word:
            if correct_word[iteration].__eq__(char):
                word_response.append(char + " correct")
            else:
                word_response.append(char + " present")
        else:
            word_response.append(char + " absent")

        # if correct_word[iteration].__eq__(char):
        #     word_response.append(char + " correct")
        # elif char in correct_word:
        #     word_response.append(char + " present")
        # else:
        #     word_response.append(char + " absent")
    return print(word_response)


def validate_word_length(guess):
    # If word is right length
    if not len(guess) == word_length:
        return print("Word is not the same length")


def validate_only_alphabetic(guess):
    # Word only contains isalpha
    if not guess.isalpha():
        return print("Word contains punctuation marks")


def validate_time(time):
    # Check if guess in 10 seconds
    if time > 10:
        return print("Turn took to long")


def validate_word(guess):
    # Check if word exists / Check if right grammar
    with open('assets/filtered_dictionaries/NL.txt', 'r') as dictionary:
        if guess not in dictionary.read():
            return print("word does not exist")