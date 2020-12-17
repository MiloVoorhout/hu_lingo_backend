"""
    This repository contains all functions connecting to the database table Games
"""

# pylint: disable=import-error
import psycopg2
from flask import abort
from openapi_server.extentions.database_singleton import DatabaseConnection


class GameRepository:
    """
    GameRepository class contains every game function that talks to the database
    """

    def __init__(self, database):
        self.conn = database

    # pylint: disable=inconsistent-return-statements
    def insert_game(self, user_id, language, game_status):
        """
        Inserts a new game into games and returns game_id
        :param user_id: user unique identifier
        :param language: language in which the game is played
        :param game_status: the length of the word
        :return: newly created id in games table aka game_id
        """
        try:
            # pylint: disable=no-else-return
            if not self._validate_game(user_id):
                curs = self.conn.cursor()
                curs.execute(
                    "INSERT INTO games (language, game_status, active, user_id, score) "
                    "VALUES(%s, %s, %s, %s, %s) RETURNING id",
                    (language, game_status, True, user_id, 0))
                game_id = curs.fetchone()[0]
                self.conn.commit()  # <- MUST commit to reflect the inserted data
                curs.close()   # <- Always close an cursor

                return game_id
            else:
                abort(409, {'message': 'There is still a game active'})
            # pylint: enable=no-else-return
        except psycopg2.OperationalError as error:
            abort(500, {'message': error})
    # pylint: enable=inconsistent-return-statements

    def _validate_game(self, user_id):
        """
        Validates if game exists based on user_id
        :param user_id: user unique identifier
        :return: boolean if game exists
        """
        curs = self.conn.cursor()
        curs.execute("SELECT EXISTS(SELECT 1 AS result "
                     "FROM games "
                     "WHERE user_id = %s AND active = TRUE)", [user_id])
        response = curs.fetchone()[0]
        curs.close()
        return response

    def _validate_game_game_id(self, game_id):
        """
        Validate a game based on game_id
        :param game_id: game unique identifier
        :return: boolean if game exists
        """
        curs = self.conn.cursor()
        curs.execute("SELECT EXISTS(SELECT 1 AS result "
                     "FROM games "
                     "WHERE id = %s AND active = TRUE)", [game_id])
        response = curs.fetchone()[0]
        curs.close()
        return response

    # pylint: disable=inconsistent-return-statements
    def get_game_round_information(self, user_id):
        """
        Get all information of a game based on user_id
        :param user_id: user unique identifier
        :return: game information
        """
        try:
            if self._validate_game(user_id):
                curs = self.conn.cursor()
                curs.execute("SELECT g.id, g.language, g.game_status, r.word, r.id, t.started_at "
                             "FROM games g "
                             "JOIN rounds r ON r.game_id = g.id "
                             "JOIN turns t ON t.round_id = r.id "
                             "WHERE g.user_id = %s "
                             "AND g.active IS TRUE AND r.active IS TRUE "
                             "AND r.active IS TRUE AND t.guessed_word IS NULL", [user_id])
                row = curs.fetchone()
                curs.close()  # <- Always close an cursor

                return {'game_id': row[0], 'game_language': row[1], 'word_length': row[2],
                        'correct_word': row[3], 'round_id': row[4], 'turn_start_time': row[5]}

        except psycopg2.OperationalError as error:
            abort(500, {'message': error})
    # pylint: enable=inconsistent-return-statements

    # pylint: disable=inconsistent-return-statements
    def get_game_information(self, user_id):
        """
        Get basic game information like the word length
        :param user_id: user unique identifier
        :return: game_id and game_status
        """
        try:
            if self._validate_game(user_id):
                curs = self.conn.cursor()
                curs.execute("SELECT g.id, g.game_status, g.language "
                             "FROM games g "
                             "WHERE g.user_id = %s AND g.active = TRUE", [user_id])
                row = curs.fetchone()
                curs.close()  # <- Always close an cursor

                return {'game_id': row[0], 'word_length': row[1], 'language': row[2]}

        except psycopg2.OperationalError as error:
            abort(500, {'message': error})
    # pylint: enable=inconsistent-return-statements

    def update_game_word_length(self, game_id, new_length):
        """
        Update game status
        :param game_id: game unique identifier
        :param new_length: new game length
        :return: Nothing
        """
        try:
            if self._validate_game_game_id(game_id):
                curs = self.conn.cursor()
                curs.execute("UPDATE public.games "
                             "SET game_status = %s "
                             "WHERE id = %s "
                             "AND active=TRUE",
                             (new_length, game_id))
                self.conn.commit()  # <- MUST commit to reflect the inserted data
                curs.close()  # <- Always close an cursor

        except psycopg2.OperationalError as error:
            abort(500, error)

    def update_game_score(self, game_id):
        """
        Update the game score
        :param game_id: game unique identifier
        :return: Nothing
        """
        try:
            if self._validate_game_game_id(game_id):
                curs = self.conn.cursor()
                curs.execute("UPDATE public.games "
                             "SET score = score + 1 "
                             "WHERE id = %s "
                             "AND active=TRUE",
                             [game_id])
                self.conn.commit()  # <- MUST commit to reflect the inserted data
                curs.close()  # <- Always close an cursor

        except psycopg2.OperationalError as error:
            abort(500, error)

    def update_end_game(self, game_id):
        """
        Update the game active to false
        :param game_id: game unique identifier
        :return: Nothing
        """
        try:
            if self._validate_game_game_id(game_id):
                curs = self.conn.cursor()
                curs.execute("UPDATE public.games "
                             "SET active = FALSE "
                             "WHERE id = %s "
                             "AND active=TRUE",
                             [game_id])
                self.conn.commit()  # <- MUST commit to reflect the inserted data
                curs.close()  # <- Always close an cursor

        except psycopg2.OperationalError as error:
            abort(500, error)
