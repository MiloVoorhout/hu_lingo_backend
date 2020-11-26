import json

from flask import make_response, abort

from lingo.game.application.game_logic import create_game, guess_turn, create_round


def create_game_controller(user_id):
    if type(user_id) == int:
        first_letter = create_game(user_id)
        print(first_letter)
        return make_response('Successfully created a game', 200)


def create_round_controller(user_id):
    if type(user_id) == int:
        first_letter = create_round(user_id)
        make_response(200, first_letter)


# TODO add guessed_word back
def guess_word(user_id, guessed_word):
    if type(user_id) == int:
        response = guess_turn(user_id, guessed_word)

        response_json = {
            "game_status": response[1],
            "word": response[0]
        }

        return make_response(json.dumps(response_json), 200)
    else:
        abort(404, "User_id is not a number")