from configparser import ConfigParser

import six
import jwt
import time
from werkzeug.exceptions import Unauthorized

# Get JWT secret information
config_object = ConfigParser()
config_object.read("credentials/config.ini")
jwt_info = config_object["JWT"]


def generate_token(user_id):
    timestamp = _current_timestamp()
    payload = {
        "iss": jwt_info['JWT_ISSUER'],
        "iat": int(timestamp),
        "exp": int(timestamp + int(jwt_info['JWT_LIFETIME_SECONDS'])),
        "sub": str(user_id),
    }

    return jwt.encode(payload, jwt_info['JWT_SECRET'], algorithm=jwt_info['JWT_ALGORITHM'])


def decode_token(token):
    try:
        return jwt.decode(token, jwt_info['JWT_SECRET'], algorithms=[jwt_info['JWT_ALGORITHM']])
    except JWTError as e:
        six.raise_from(Unauthorized, e)


def get_secret(user, token_info) -> str:
    return '''
    You are user_id {user} and the secret is 'wbevuec'.
    Decoded token claims: {token_info}.
    '''.format(user=user, token_info=token_info)


def _current_timestamp() -> int:
    return int(time.time())
