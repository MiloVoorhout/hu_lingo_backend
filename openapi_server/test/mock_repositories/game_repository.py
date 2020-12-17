"""
    This repository contains all test functions for GameRepository
"""

# pylint: disable=import-error
from datetime import datetime, timedelta


class TestGameRepository:
    """
    This is a test repository created only for the soul purpose of testing
    """

    def __init__(self):
        self.conn = 'DatabaseConnection'

    def insert_game(self, user_id, language, game_status):
        """
        Inserts a new game into games and returns game_id
        :param user_id: user unique identifier
        :param language: language in which the game is played
        :param game_status: the length of the word
        :return: newly created id in games table aka game_id
        """
        if user_id == 1:
            return 1

    def get_game_round_information(self, user_id):
        """
        Get all information of a game based on user_id
        :param user_id: user unique identifier
        :return: game information
        """

        if user_id == 1:
            return {'game_id': 1, 'game_language': 'NL', 'word_length': 5,
                    'correct_word': 'TESTS', 'round_id': 1, 'turn_start_time': (datetime.now() - timedelta(seconds=10))}
        elif user_id == 2:
            return {'game_id': 1, 'game_language': 'NL', 'word_length': 7,
                    'correct_word': 'ANDROID', 'round_id': 1, 'turn_start_time': (datetime.now() - timedelta(seconds=12))}
        elif user_id == 4:
            return {'game_id': 4, 'game_language': 'NL', 'word_length': 5,
                    'correct_word': 'TESTS', 'round_id': 4, 'turn_start_time': (datetime.now() - timedelta(seconds=10))}

    # pylint: disable=inconsistent-return-statements
    def get_game_information(self, user_id):
        """
        Get basic game information like the word length
        :param user_id: user unique identifier
        :return: game_id and game_status
        """
        if user_id == 1:
            return {'game_id': 1, 'word_length': 5}
        if user_id == 5:
            return {'game_id': 2, 'word_length': 5}


    def update_game_word_length(self, game_id, new_length):
        """
        Update game status
        :param game_id: game unique identifier
        :param new_length: new game length
        :return: Nothing
        """
        return ''

    def update_game_score(self, game_id):
        """
        Update the game score
        :param game_id: game unique identifier
        :return: Nothing
        """
        return ''

    def update_end_game(self, game_id):
        """
        Update the game active to false
        :param game_id: game unique identifier
        :return: Nothing
        """
        return ''
