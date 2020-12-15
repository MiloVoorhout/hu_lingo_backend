"""
    This controller contains all functions for game controller
"""

# pylint: disable=import-error
import json
from flask import make_response, abort
from openapi_server.core.application.game.game_logic import GameService
from openapi_server.core.port.data.game_repository import GameRepository
from openapi_server.core.port.data.round_repository import RoundRepository
from openapi_server.core.port.data.turn_repository import TurnRepository
from openapi_server.core.port.file.word_repository import WordRepository

game_repository = GameRepository()
round_repository = RoundRepository()
turn_repository = TurnRepository(round_repository)
word_repository = WordRepository()
game_service = GameService(game_repository, round_repository, turn_repository, word_repository)


# pylint: disable=inconsistent-return-statements
def create_game_controller(user, language):
    """
    Creates a game based on user_id
    :param language: language the game is played in
    :param user: user unique identifier
    :return: first letter of word and word length
    """

    # Turn Bearer token info into a integer
    user_id = int(user)
    if isinstance(user_id, int):
        first_letter = game_service.create_game(user_id, language)

        response_json = {
            'first_letter': first_letter[0],
            'game_length': first_letter[1]
        }

        return make_response(json.dumps(response_json), 200)
# pylint: enable=inconsistent-return-statements


# pylint: disable=inconsistent-return-statements
def create_round_controller(user):
    """
    Creates a new round based on user_id
    :param user: user unique identifier
    :return: first letter and game length
    """

    # Turn Bearer token info into a integer
    user_id = int(user)
    if isinstance(user_id, int):
        first_letter = game_service.create_round(user_id)

        response_json = {
            'first_letter': first_letter[0],
            'game_length': first_letter[1]
        }

        return make_response(json.dumps(response_json), 200)
# pylint: enable=inconsistent-return-statements


# pylint: disable=fixme
# TODO add guessed_word back
# pylint: enable=fixme
# pylint: disable=inconsistent-return-statements
def guess_word(user, guessed_word):
    """
    Do a turn guess
    :param user: user unique identifier
    :param guessed_word: users guess
    :return: game status, word response, (validation error)
    """

    # Turn Bearer token info into a integer
    user_id = int(user)

    # pylint: disable=no-else-return
    if isinstance(user_id, int):
        response = game_service.guess_turn(user_id, guessed_word)

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
