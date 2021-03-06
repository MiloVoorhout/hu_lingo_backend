"""
    This scripts runs all validations for the game_logic
"""
from openapi_server.core.domain.game.validation import validate_word, validate_only_alphabetic, \
    validate_word_length, validate_time


def run_all_turn_validations(guess, correct_word_length, start_time, request_time, game_language):
    """
    Validation constructor, runs all validations in this file
    :param guess: Users guess word
    :param correct_word_length: The length that the guess needs to be
    :param start_time: Start_time is the start time of the turn
    :param request_time: Time when user started the call
    :param game_language: Language of the game
    :return: Boolean = If there has been an error / Str = the error message
    """

    error_messages = [validate_word(guess, game_language),
                      validate_only_alphabetic(guess),
                      validate_word_length(guess, correct_word_length),
                      validate_time(start_time, request_time)]

    return error_messages
