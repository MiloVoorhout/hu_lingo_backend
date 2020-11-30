"""
    This script handles everything for the authentication.
    The authentication is made with a JWT token.
"""

# pylint: disable=import-error
from configparser import ConfigParser
import six
import time
import jwt
from werkzeug.exceptions import Unauthorized

# Get JWT secret information
config_object = ConfigParser()
config_object.read("credentials/config.ini")
jwt_info = config_object["JWT"]


def generate_token(user_id):
    """
    Generates JWT token based on user_id and more
    :param user_id: User unique identifier - Integer
    :return: Encoded JWT token
    """
    timestamp = _current_timestamp()
    payload = {
        "iss": jwt_info['JWT_ISSUER'],
        "iat": int(timestamp),
        "exp": int(timestamp + int(jwt_info['JWT_LIFETIME_SECONDS'])),
        "sub": str(user_id),
    }

    return jwt.encode(payload, jwt_info['JWT_SECRET'], algorithm=jwt_info['JWT_ALGORITHM'])


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
