def validate_word_length(guess, word_length):
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
