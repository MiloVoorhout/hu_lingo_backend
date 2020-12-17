"""
    This repository contains all functions connecting to the database table Turns
"""

# pylint: disable=import-error
import psycopg2
from flask import abort


class TurnRepository:
    """
    TurnRepository class contains every turn function that talks to the database
    """

    def __init__(self, round_repository, database):
        self.conn = database
        self.round_repository = round_repository

    # pylint: disable=inconsistent-return-statements
    def insert_turn(self, round_id):
        """
        Insert new turn into turn table
        :param round_id: round unique identifier
        :return: boolean value if commit was good
        """
        try:
            # pylint: disable=no-else-return
            if self.round_repository.validate_round_round_id(round_id):
                curs = self.conn.cursor()
                curs.execute("INSERT INTO turns (guessed_word, started_at, round_id) "
                             "VALUES(NULL, now()::timestamptz, %s)", [round_id])
                self.conn.commit()  # <- MUST commit to reflect the inserted data
                curs.close()   # <- Always close an cursor

                return True
            else:
                abort(404, {'message': 'No active round found'})
            # pylint: enable=no-else-return
        except psycopg2.OperationalError as error:
            abort(500, {'message': error})
    # pylint: enable=inconsistent-return-statements

    def update_turn(self, guessed_word, round_id):
        """
        Update guessed word of turn
        :param guessed_word: users guess
        :param round_id: round unique identifier
        :return: Nothing
        """
        try:
            if self.round_repository.validate_round_round_id(round_id):
                curs = self.conn.cursor()
                curs.execute("UPDATE public.turns "
                             "SET guessed_word=%s "
                             "WHERE round_id = %s "
                             "AND guessed_word IS NULL",
                             (guessed_word, round_id))
                self.conn.commit()  # <- MUST commit to reflect the inserted data
                curs.close()  # <- Always close an cursor

            else:
                abort(404, {'message': 'No active round found'})
        except psycopg2.OperationalError as error:
            abort(500, error)

    # pylint: disable=inconsistent-return-statements
    def get_turn_count(self, round_id):
        """
        Get amount of turns of round
        :param round_id: round unique identifier
        :return: return amount of turns
        """
        try:
            if self.round_repository.validate_round_round_id(round_id):
                curs = self.conn.cursor()
                curs.execute("SELECT COUNT(*) FROM turns WHERE round_id = %s;", [round_id])
                response = curs.fetchone()[0]
                curs.close()
                return response
        except psycopg2.OperationalError as error:
            abort(500, error)
    # pylint: enable=inconsistent-return-statements
