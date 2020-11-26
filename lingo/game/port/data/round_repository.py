import psycopg2
from flask import abort
from lingo.extentions.database_singleton import DatabaseConnection

conn = DatabaseConnection.get_connection(DatabaseConnection)


# Insert Round
def insert_round(game_id, random_word):
    try:
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
    except psycopg2.OperationalError as e:
        abort(500, {'message': e})


def validate_round(game_id):
    curs = conn.cursor()
    curs.execute("SELECT EXISTS(SELECT 1 AS result FROM rounds WHERE game_id = %s AND active = TRUE)", [game_id])
    response = curs.fetchone()[0]
    curs.close()
    return response


# TODO: Change name of function
def validate_round_round_id(round_id):
    curs = conn.cursor()
    curs.execute("SELECT EXISTS(SELECT 1 AS result FROM rounds WHERE id = %s and active = TRUE)", [round_id])
    response = curs.fetchone()[0]
    curs.close()
    return response


def update_round_finished(game_id):
    try:
        if not validate_round(game_id):
            curs = conn.cursor()
            curs.execute("UPDATE public.rounds "
                         "SET active=FALSE "
                         "WHERE game_id = %s "
                         "AND active=TRUE",
                         [game_id])
            conn.commit()  # <- MUST commit to reflect the inserted data
            curs.close()  # <- Always close an cursor

    except psycopg2.OperationalError as e:
        abort(500, e)


def update_end_round(round_id):
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

    except psycopg2.OperationalError as e:
        abort(500, e)