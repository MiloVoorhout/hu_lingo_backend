import json

from flask import make_response

from lingo.game.application.game_logic import create_game, guess_turn


def create_game_controller(user_id):
    if type(user_id) == int:
        create_game(user_id)
        print("Hallo het is gelukt")
        return make_response('Successfully created a game', 200)


# TODO add guessed_word back
def guess_word(user_id, guessed_word):
    if type(user_id) == int:
        response = guess_turn(user_id, guessed_word)

        response_json = {
            "game_status": response[1],
            "word": response[0]
        }

        return make_response(json.dumps(response_json), 200)
