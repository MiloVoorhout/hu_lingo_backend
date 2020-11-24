import time
from datetime import datetime
from flask import abort

from lingo.game.port.data.game_repository import get_start_time_turn

failed = False
fail_message = ''


def run_all_turn_validations(guess, correct_word_length, round_id, request_time):
    set_fail(False, '')

    validate_word(guess)
    if not failed:
        validate_only_alphabetic(guess)
        if not failed:
            validate_word_length(guess, correct_word_length)
            if not failed:
                validate_time(round_id, request_time)

    return failed, fail_message


def validate_word(guess):
    # Check if word exists / Check if right grammar
    with open('assets/filtered_dictionaries/NL.txt', 'r') as dictionary:
        guess = guess.lower()
        if guess not in dictionary.read():
            set_fail(True, "Given word does not exist")


def validate_only_alphabetic(guess):
    # Word only contains isalpha
    if not guess.isalpha():
        set_fail(True, "Word contains punctuation marks")


def validate_word_length(guess, word_length):
    # If word is right length
    if not len(guess) == word_length:
        set_fail(True, "Word is not the same length")


def validate_time(round_id, now):
    # Make date time from NOW variable
    current_time = datetime.strptime(now, "%Y-%b-%d %H:%M:%S.%f")

    # Get start time of latest turn
    start_time = get_start_time_turn(round_id)

    print(start_time)

    # Calculate the difference between date/times
    difference = current_time - start_time

    # Check if guess in 10 seconds
    # TODO: change time difference to 10 seconds
    if difference.seconds > 10000000:
        set_fail(True, "Turn took longer than 10 seconds")


def set_fail(status, message):
    global failed, fail_message
    failed = status
    fail_message = message


