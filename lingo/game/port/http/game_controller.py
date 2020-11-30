import json

from flask import make_response, abort

from lingo.game.application.game_logic import create_game, guess_turn, create_round


def create_game_controller(user_id):
    user_id = int(user_id)
    if type(user_id) == int:
        first_letter = create_game(user_id)

        response_json = {
            'first_letter': first_letter[0],
            'game_length': first_letter[1]
        }

        return make_response(json.dumps(response_json), 200)


def create_round_controller(user_id):
    if type(user_id) == int:
        first_letter = create_round(user_id)

        response_json = {
            'first_letter': first_letter[0],
            'game_length': first_letter[1]
        }

        make_response(json.dumps(response_json), 200)


# TODO add guessed_word back
def guess_word(user_id, guessed_word):
    if type(user_id) == int:
        response = guess_turn(user_id, guessed_word)
        print(response)

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

