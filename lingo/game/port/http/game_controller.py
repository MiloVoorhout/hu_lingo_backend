"""
    This controller contains all functions for game controller
"""

# pylint: disable=import-error
import json
from flask import make_response, abort
from lingo.game.application.game_logic import create_game, guess_turn, create_round


# pylint: disable=inconsistent-return-statements
def create_game_controller(user_id):
    """
    Creates a game based on user_id
    :param user_id: user unique identifier
    :return: first letter of word and word length
    """
    user_id = int(user_id)
    if isinstance(user_id, int):
        first_letter = create_game(user_id)

        response_json = {
            'first_letter': first_letter[0],
            'game_length': first_letter[1]
        }

        return make_response(json.dumps(response_json), 200)
# pylint: enable=inconsistent-return-statements


# pylint: disable=inconsistent-return-statements
def create_round_controller(user_id):
    """
    Creates a new round based on user_id
    :param user_id: user unique identifier
    :return: first letter and game length
    """
    if isinstance(user_id, int):
        first_letter = create_round(user_id)

        response_json = {
            'first_letter': first_letter[0],
            'game_length': first_letter[1]
        }

        return make_response(json.dumps(response_json), 200)
# pylint: enable=inconsistent-return-statements


# TODO add guessed_word back
# pylint: disable=inconsistent-return-statements
def guess_word(user_id, guessed_word):
    """
    Do a turn guess
    :param user_id: user unique identifier
    :param guessed_word: users guess
    :return: game status, word response, (validation error)
    """
    # pylint: disable=no-else-return
    if isinstance(user_id, int):
        response = guess_turn(user_id, guessed_word)

        if response[0].__eq__('abort'):
            abort(404, 'An error occured')
        if len(response) == 3:
            response_json = {
                    "game_status": response[0],
                    "word": response[1],
                    "validation_error": response[2]
                }
        else:
            response_json = {
                    "game_status": response[0],
                    "word": response[1]
                }

        return make_response(json.dumps(response_json), 200)

    else:
        abort(404, 'User_id is not a number')
    # pylint: enable=no-else-return
# pylint: enable=inconsistent-return-statements
