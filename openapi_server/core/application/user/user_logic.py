"""
    This scripted is made as an User Service a bridge between controller and domain
"""

# pylint: disable=import-error
from passlib.handlers.sha2_crypt import sha256_crypt


class UserService:
    """
    UserService class contains all logic connections between port and domain
    """

    def __init__(self, user_repository):
        self.user_repository = user_repository

    def create_user(self, username, password):
        """
        Creates a gamed based on user_id
        :param username: user unique identifier
        :param password: users password
        :return: boolean
        """
        password_crypt = sha256_crypt.hash(password)

        if self.user_repository.insert_user(username, password_crypt):
            return True

        return False

    def check_user_login(self, username, password):
        """
        Creates a gamed based on user_id
        :param username: user unique identifier
        :param password: users password
        :return: user_id
        """
        user_details = self.user_repository.get_user_details(username)
        if sha256_crypt.verify(password, user_details['password']):
            return user_details['user_id']

        return None

    def user_high_scores(self, user_id):
        """
        Creates a gamed based on user_id
        :param user_id: user unique identifier
        :return: list of users high scores
        """

        scores = self.user_repository.get_high_scores(user_id)
        return scores
