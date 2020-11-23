from flask import make_response

from lingo.extentions.database_singleton import DatabaseConnection
from lingo.game.application.game_logic import create_game


def create_game_controller(user_id):
    if type(user_id) == int:
        if create_game(user_id):
            DatabaseConnection.get_connection(DatabaseConnection).commit()
            return make_response('Successfully created a game', 200)
