# pylint: skip-file
"""
    This repository contains all functions connecting to the database table Turns
"""


class TestTurnRepository:
    """
    TurnRepository class contains every turn function that talks to the database
    """

    def __init__(self, round_repository):
        self.conn = 'DatabaseConnection'
        self.round_repository = round_repository

    def insert_turn(self, round_id):
        """
        Insert new turn into turn table
        :param round_id: round unique identifier
        :return: boolean value if commit was good
        """
        return True

    def update_turn(self, guessed_word, round_id):
        """
        Update guessed word of turn
        :param guessed_word: users guess
        :param round_id: round unique identifier
        :return: Nothing
        """
        return ''

    def get_turn_count(self, round_id):
        """
        Get amount of turns of round
        :param round_id: round unique identifier
        :return: return amount of turns
        """
        if round_id == 1:
            return 2
        elif round_id == 4:
            return 5
