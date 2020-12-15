"""
    This scripted is made as an Game Domain in
    here all game data is manipulated an analysed
"""
# pylint: disable=too-many-arguments
from openapi_server.core.application.game.validation_logic import run_all_turn_validations


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

    return word_guess, character_response, ""
# pylint: enable=too-many-arguments


def check_characters(guessed_word, correct_word):
    """
    Check all characters of the word
    :param guessed_word: Users guessed word
    :param correct_word: Correct word of the round
    :return: Character lis and if they are correct, present or absent
    """
    word_response = [{"letter": char, "letterFeedback": "absent"} for char in guessed_word.upper()]
    guessed_characters = list(guessed_word.upper())
    correct_characters = list(correct_word.upper())

    if guessed_word.__eq__(correct_word):
        for char in word_response:
            char["letterFeedback"] = "correct"
    else:
        for iteration, char in enumerate(guessed_characters):
            if char == correct_characters[iteration]:
                word_response[iteration]["letterFeedback"] = "correct"
                guessed_characters[iteration] = "-"
                correct_characters[iteration] = "-"

        for guess_iteration, guess_char in enumerate(guessed_characters):
            if not guess_char.__eq__("-"):
                for correct_iteration, correct_char in enumerate(correct_characters):
                    if not correct_char.__eq__("-") and correct_char.__eq__(guess_char):
                        word_response[guess_iteration]["letterFeedback"] = "present"
                        guessed_characters[guess_iteration] = "-"
                        correct_characters[correct_iteration] = "-"

    return word_response


def invalid_characters(guessed_word):
    """
    Say that every character is invalid
    :param guessed_word: users guessed word
    :return: List of character with every character invalid
    """
    word_response = []

    for char in guessed_word:
        word_response.append(
            {
                "letter": char,
                "letterFeedback": "invalid"
            }
        )

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
