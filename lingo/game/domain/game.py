"""
    This scripted is made as an Game Domain in
    here all game data is manipulated an analysed
"""
import json

from lingo.game.application.validation_logic import run_all_turn_validations


# pylint: disable=too-many-arguments
def run_turn(guessed_word, correct_word, word_length,
             turn_start_time, now, turn_count, game_language):
    """
    Run everything to do with a guess turn
    :param guessed_word: Users guessed word
    :param correct_word: The correct word
    :param word_length: The correct word length
    :param turn_start_time: Start time of current turn
    :param now: Time the http call started
    :param turn_count: Count of all turns this round
    :param game_language: The language of the game
    :return: turn result, character response, (validation errors)
    """
    # First check validations
    validation_response = run_all_turn_validations(guessed_word, word_length,
                                                   turn_start_time, now, game_language)
    validation = check_validation_response(validation_response)
    word_guess = ''
    character_response = ''

    if not validation[0]:
        character_response = check_characters(guessed_word, correct_word)

        if correct_word.__eq__(guessed_word):
            word_guess = 'correct'
        else:
            word_guess = 'next-round'

    if turn_count >= 5:
        if validation[0]:
            return 'game-over', character_response, validation[1]

        word_guess = 'game-over'
    else:
        if validation[0]:
            character_response = invalid_characters(guessed_word)
            return 'validation-error', character_response, validation[1]

    return word_guess, character_response
# pylint: enable=too-many-arguments


def check_characters(guessed_word, correct_word):
    """
    Check all characters of the word
    :param guessed_word: Users guessed word
    :param correct_word: Correct word of the round
    :return: Character lis and if they are correct, present or absent
    """
    word_response = []
    checked_characters = []

    # Change word to CAPS
    guess = guessed_word.upper()
    for iteration, char in enumerate(guess):
        if char in correct_word:
            if correct_word[iteration].__eq__(char):
                check_answer = "correct"
                # word_response.append(char + " correct")
            else:
                check_answer = "present"
                # word_response.append(char + " present")
        else:
            check_answer = "absent"
            # word_response.append(char + " absent")

        # TODO: first letter can be present second letter correct fix this
        if char in checked_characters and not check_answer.__eq__("correct"):
            check_answer = "absent"

        word_response.append(
            {
                "letter": char,
                "letterFeedback": check_answer
            }
        )
        checked_characters.append(char)

    return word_response


def invalid_characters(guessed_word):
    """
    Say that every character is invalid
    :param guessed_word: users guessed word
    :return: List of character with every character invalid
    """
    word_response = []

    for char in guessed_word:
        word_response.append(char + " invalid")

    return word_response


def check_validation_response(validation_response):
    """
    Check validation responses
    :param validation_response: response of the validation check
    :return: validation error and the messages
    """
    validation_error = False
    error_message = []
    for response in validation_response:
        if len(response) > 0:
            validation_error = True
            error_message.append(response)

    return validation_error, error_message
