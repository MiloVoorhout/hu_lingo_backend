"""
    This script handles everything for the authentication.
    The authentication is made with a JWT token.
"""

# pylint: disable=import-error
import os
import time
import six
import jwt
from flask import make_response
from werkzeug.exceptions import Unauthorized

# Get JWT secret information
from openapi_server.core.port.data.auth.user_repository import get_user_id_login


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
            "iss": os.environ.get("JWT_ISSUER"),
            "iat": int(timestamp),
            "exp": int(timestamp + int(os.environ.get("JWT_LIFETIME_SECONDS"))),
            "sub": str(user_id),
        }

        return make_response(jwt.encode(payload, os.environ.get("JWT_SECRET"),
                                        algorithm=os.environ.get("JWT_ALGORITHM")), 200)

    return make_response("User not found", 404)


def decode_token(token):
    """
    Decodes JWT token that is given to http request
    :param token: JWT Token
    :return: Decoded JWT Token
    """
    try:
        return jwt.decode(token, os.environ.get("JWT_SECRET"),
                          algorithms=[os.environ.get("JWT_ALGORITHM")])
    except jwt.DecodeError as error:
        six.raise_from(Unauthorized, error)


def _current_timestamp() -> int:
    return int(time.time())


def check_token(token_info):
    """
    Check if token in expired
    :param token_info: JWT Token information
    :return: 200 or 401 status code
    """
    if not _current_timestamp() > token_info['exp']:
        return make_response('', 200)

    return make_response('', 401)
