"""
    This script handles everything for the authentication.
    The authentication is made with a JWT token.
"""

# pylint: disable=import-error
import json
from configparser import ConfigParser
import six
import time
import jwt
from flask import make_response
from werkzeug.exceptions import Unauthorized

# Get JWT secret information
from lingo.auth.user_repository import get_user_id_login

config_object = ConfigParser()
config_object.read("credentials/config.ini")
jwt_info = config_object["JWT"]


def generate_token(username, password):
    """
    Generates JWT token based on user_id and more
    :param username: User unique name identifier - String
    :param password: User password - String
    :return: Encoded JWT token
    """

    user_id = get_user_id_login(username, password)

    if user_id is not None:
        timestamp = _current_timestamp()
        payload = {
            "iss": jwt_info['JWT_ISSUER'],
            "iat": int(timestamp),
            "exp": int(timestamp + int(jwt_info['JWT_LIFETIME_SECONDS'])),
            "sub": str(user_id),
        }

        return make_response(jwt.encode(payload, jwt_info['JWT_SECRET'], algorithm=jwt_info['JWT_ALGORITHM']), 200)
    else:
        return make_response("User not found", 404)


def decode_token(token):
    """
    Decodes JWT token that is given to http request
    :param token: JWT Token
    :return: Decoded JWT Token
    """
    try:
        return jwt.decode(token, jwt_info['JWT_SECRET'], algorithms=[jwt_info['JWT_ALGORITHM']])
    except jwt.DecodeError as error:
        six.raise_from(Unauthorized, error)


# TODO: Delete function
def get_secret(user, token_info) -> str:
    """
    Test function to see if JWT token works
    :param user: user
    :param token_info:
    :return:
    """
    return '''
    You are user_id {user} and the secret is 'wbevuec'.
    Decoded token claims: {token_info}.
    '''.format(user=user, token_info=token_info)


def _current_timestamp() -> int:
    return int(time.time())


def check_token(token_info):
    if not _current_timestamp() > token_info['exp']:
        return make_response('', 200)
    else:
        return make_response('', 401)
