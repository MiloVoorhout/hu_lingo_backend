"""
    This repository contains all functions connecting to the database table Round
"""

# pylint: disable=import-error
import psycopg2
from flask import abort
from lingo.extentions.database_singleton import DatabaseConnection

# Singleton database connection
conn = DatabaseConnection.get_connection(DatabaseConnection)


# pylint: disable=inconsistent-return-statements
def insert_round(game_id, random_word):
    """
    Insert a new round into round table
    :param game_id: game unique identifier
    :param random_word: random word to insert
    :return: round id
    """
    try:
        # pylint: disable=no-else-return
        if not validate_round(game_id):
            curs = conn.cursor()
            curs.execute("INSERT INTO rounds (active, word, game_id) "
                         "VALUES(%s, %s, %s) RETURNING id",
                         (True, random_word, game_id))
            round_id = curs.fetchone()
            conn.commit()  # <- MUST commit to reflect the inserted data
            curs.close()   # <- Always close an cursor

            return round_id
        else:
            abort(409, {'message': 'There is still a round active'})
        # pylint: enable=no-else-return
    except psycopg2.OperationalError as error:
        abort(500, {'message': error})
# pylint: enable=inconsistent-return-statements


def validate_round(game_id):
    """
    Validate if round exists with game_id
    :param game_id: game unique identifier
    :return: boolean if round exists
    """
    curs = conn.cursor()
    curs.execute("SELECT EXISTS(SELECT 1 AS result "
                 "FROM rounds "
                 "WHERE game_id = %s AND active = TRUE)", [game_id])
    response = curs.fetchone()[0]
    curs.close()
    return response


def validate_round_round_id(round_id):
    """
    Validate if round exists with round_id
    :param round_id: round unique identifier
    :return: boolean if round exists
    """
    curs = conn.cursor()
    curs.execute("SELECT EXISTS(SELECT 1 AS result "
                 "FROM rounds "
                 "WHERE id = %s and active = TRUE)", [round_id])
    response = curs.fetchone()[0]
    curs.close()
    return response


def update_end_round(round_id):
    """
    Update active of round to false
    :param round_id: round unique identifier
    :return: Nothing
    """
    try:
        if validate_round_round_id(round_id):
            curs = conn.cursor()
            curs.execute("UPDATE public.rounds "
                         "SET active = FALSE "
                         "WHERE id = %s "
                         "AND active=TRUE",
                         [round_id])
            conn.commit()  # <- MUST commit to reflect the inserted data
            curs.close()  # <- Always close an cursor

    except psycopg2.OperationalError as error:
        abort(500, error)
