import psycopg2
from flask import abort
from datetime import datetime
from lingo.extentions.database_singleton import DatabaseConnection

conn = DatabaseConnection.get_connection(DatabaseConnection)


# Insert Game
def insert_game(user_id, language, game_status):
    try:
        if not validate_game(user_id):
            curs = conn.cursor()
            curs.execute(
                "INSERT INTO games (language, game_status, active, user_id, score) "
                "VALUES(%s, %s, %s, %s, %s) RETURNING id",
                (language, game_status, True, user_id, 0))
            game_id = curs.fetchone()[0]
            conn.commit()  # <- MUST commit to reflect the inserted data
            curs.close()

            return game_id
        else:
            abort(409, {'message': 'There is still a game active'})
    except psycopg2.OperationalError as e:
        abort(500, {'message': e})


def validate_game(user_id):
    curs = conn.cursor()
    curs.execute("SELECT EXISTS(SELECT 1 AS result FROM games WHERE user_id = %s AND active = TRUE)", [user_id])
    response = curs.fetchone()[0]
    curs.close()
    return response


# Insert Round
def insert_round(game_id, random_word):
    try:
        if not validate_round(game_id):
            curs = conn.cursor()
            curs.execute("INSERT INTO rounds (active, word, game_id) "
                         "VALUES(%s, %s, %s) RETURNING id",
                         (True, random_word, game_id))
            round_id = curs.fetchone()[0]
            conn.commit()  # <- MUST commit to reflect the inserted data
            curs.close()  # <- Always close an

            return round_id
        else:
            abort(409, {'message': 'There is still a round active'})
    except psycopg2.OperationalError as e:
        abort(500, {'message': e})


def validate_round(game_id):
    curs = conn.cursor()
    curs.execute("SELECT EXISTS(SELECT 1 AS result FROM rounds WHERE game_id = %s AND active = TRUE)", [game_id])
    response = curs.fetchone()[0]
    curs.close()
    return response


# TODO: Change name of function
def test_round(round_id):
    curs = conn.cursor()
    curs.execute("SELECT EXISTS(SELECT 1 AS result FROM rounds WHERE id = %s and active = TRUE)", [round_id])
    response = curs.fetchone()[0]
    curs.close()
    return response


# Insert Turn
def insert_turn(round_id):
    try:
        if test_round(round_id):
            start_time = datetime.timestamp(datetime.now())
            curs = conn.cursor()
            curs.execute("INSERT INTO turns (guessed_word, started_at, round_id) VALUES(%s, %s, %s)",
                         ('', start_time, round_id))
            conn.commit()  # <- MUST commit to reflect the inserted data
            curs.close()  # <- Always close an

            return True
        else:
            abort(404, {'message': 'No active round found'})
    except psycopg2.OperationalError as e:
        abort(500, {'message': e})
