import json

import psycopg2
from flask import abort
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
            curs.close()   # <- Always close an cursor

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


def validate_game_game_id(game_id):
    curs = conn.cursor()
    curs.execute("SELECT EXISTS(SELECT 1 AS result FROM games WHERE id = %s AND active = TRUE)", [game_id])
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


# Get game information
def get_game_information(user_id):
    try:
        if validate_game(user_id):
            curs = conn.cursor()
            curs.execute("SELECT g.id, g.game_status, r.word, r.id "
                         "FROM games g "
                         "JOIN rounds r ON r.game_id = g.id "
                         "WHERE g.user_id = %s AND g.active = TRUE", [user_id])
            row = curs.fetchone()
            curs.close()  # <- Always close an cursor

            return {'game_id': row[0], 'word_length': row[1], 'correct_word': row[2], 'round_id': row[3]}

    except psycopg2.OperationalError as e:
        abort(500, {'message': e})


def get_start_time_turn(round_id):
    try:
        if test_round(round_id):
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
        if test_round(round_id):
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


def update_game_word_length(game_id, new_length):
    try:
        if validate_game_game_id(game_id):
            curs = conn.cursor()
            curs.execute("UPDATE public.games "
                         "SET game_status = %s "
                         "WHERE id = %s "
                         "AND active=TRUE",
                         (new_length, game_id))
            conn.commit()  # <- MUST commit to reflect the inserted data
            curs.close()  # <- Always close an cursor

    except psycopg2.OperationalError as e:
        abort(500, e)


def update_end_round(round_id):
    try:
        if test_round(round_id):
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


def update_game_score(game_id):
    try:
        if validate_game_game_id(game_id):
            curs = conn.cursor()
            curs.execute("UPDATE public.games "
                         "SET score = score + 1 "
                         "WHERE id = %s "
                         "AND active=TRUE",
                         [game_id])
            conn.commit()  # <- MUST commit to reflect the inserted data
            curs.close()  # <- Always close an cursor

    except psycopg2.OperationalError as e:
        abort(500, e)


def get_turn_count(round_id):
    try:
        if test_round(round_id):
            curs = conn.cursor()
            curs.execute("SELECT COUNT(*) FROM turns WHERE round_id = %s;", [round_id])
            response = curs.fetchone()[0]
            curs.close()
            return response
    except psycopg2.OperationalError as e:
        abort(500, e)


def update_end_game(game_id):
    try:
        if validate_game_game_id(game_id):
            curs = conn.cursor()
            curs.execute("UPDATE public.games "
                         "SET active = FALSE "
                         "WHERE id = %s "
                         "AND active=TRUE",
                         [game_id])
            conn.commit()  # <- MUST commit to reflect the inserted data
            curs.close()  # <- Always close an cursor

    except psycopg2.OperationalError as e:
        abort(500, e)
