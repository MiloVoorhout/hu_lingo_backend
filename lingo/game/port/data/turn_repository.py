import psycopg2
from flask import abort
from lingo.extentions.database_singleton import DatabaseConnection
from lingo.game.port.data.round_repository import validate_round_round_id

conn = DatabaseConnection.get_connection(DatabaseConnection)


# Insert Turn
def insert_turn(round_id):
    try:
        if validate_round_round_id(round_id):
            curs = conn.cursor()
            curs.execute("INSERT INTO turns (guessed_word, started_at, round_id) VALUES(%s, now()::timestamptz, %s)",
                         ('', round_id))
            conn.commit()  # <- MUST commit to reflect the inserted data
            curs.close()   # <- Always close an cursor

            return True
        else:
            abort(404, {'message': 'No active round found'})
    except psycopg2.OperationalError as e:
        abort(500, {'message': e})


def get_start_time_turn(round_id):
    try:
        if validate_round_round_id(round_id):
            curs = conn.cursor()
            curs.execute("SELECT t.started_at, t.id "
                         "FROM turns t "
                         "WHERE t.round_id = %s "
                         "AND t.guessed_word = ''", [round_id])
            response = curs.fetchone()
            curs.close()  # <- Always close an cursor

            return response[0]

    except psycopg2.OperationalError as e:
        return None


def update_turn(guessed_word, round_id):
    try:
        if validate_round_round_id(round_id):
            curs = conn.cursor()
            curs.execute("UPDATE public.turns "
                         "SET guessed_word=%s "
                         "WHERE round_id = %s "
                         "AND guessed_word = ''",
                         (guessed_word, round_id))
            conn.commit()  # <- MUST commit to reflect the inserted data
            curs.close()  # <- Always close an cursor

        else:
            abort(404, {'message': 'No active round found'})
    except psycopg2.OperationalError as e:
        abort(500, e)


def get_turn_count(round_id):
    try:
        if validate_round_round_id(round_id):
            curs = conn.cursor()
            curs.execute("SELECT COUNT(*) FROM turns WHERE round_id = %s;", [round_id])
            response = curs.fetchone()[0]
            curs.close()
            return response
    except psycopg2.OperationalError as e:
        abort(500, e)

