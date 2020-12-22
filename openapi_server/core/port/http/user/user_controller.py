"""
    This controller contains all functions for user controller
"""
# pylint: disable=import-error
import json
from flask import make_response, abort
from openapi_server.extentions.database_singleton import DatabaseConnection
from openapi_server.core.port.data.user.user_repository import UserRepository
from openapi_server.core.application.user.user_logic import UserService

database_connection = DatabaseConnection.get_connection(DatabaseConnection())
user_service = UserService(UserRepository(database_connection))


def create_new_user(username, password):
    """
    Creates a new user
    :param username: unique user identifier
    :param password: users password
    :return: status code
    """

    if user_service.create_user(username, password):
        return make_response('', 200)

    return make_response('', 400)


# pylint: disable=inconsistent-return-statements
def get_high_scores_user(user):
    """
    Creates a game based on user_id
    :param user: user unique identifier
    :return: first letter of word and word length
    """

    # Turn Bearer token info into a integer
    user_id = int(user)

    # pylint: disable=no-else-return
    if isinstance(user_id, int):
        high_scores = user_service.user_high_scores(user_id)

        response_json = {
            "high scores": high_scores
        }

        return make_response(json.dumps(response_json), 200)

    else:
        abort(404, 'User_id is not a number')
    # pylint: enable=no-else-return
# pylint: enable=inconsistent-return-statements
