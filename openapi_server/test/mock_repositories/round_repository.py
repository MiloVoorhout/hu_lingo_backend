# pylint: skip-file
"""
    This repository contains all test functions for GameRepository
"""


class TestRoundRepository:
    """
    This is a test repository created only for the soul purpose of testing
    """

    def __init__(self):
        self.conn = 'DatabaseConnection'

    def insert_round(self, game_id, random_word):
        """
        Insert a new round into round table
        :param game_id: game unique identifier
        :param random_word: random word to insert
        :return: round id
        """
        if game_id == 1:
            return 1
        if game_id == 5:
            return None

    def validate_round_round_id(self, round_id):
        """
        Validate if round exists with round_id
        :param round_id: round unique identifier
        :return: boolean if round exists
        """
        return True

    def update_end_round(self, round_id):
        """
        Update active of round to false
        :param round_id: round unique identifier
        :return: Nothing
        """
        return ''
