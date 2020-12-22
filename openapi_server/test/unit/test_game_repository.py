import unittest
from contextlib import closing
import datetime

import psycopg2
import testing.postgresql

from openapi_server.core.port.data.game.game_repository import GameRepository


class TestGameRepository(unittest.TestCase):
    pgsql = None
    conn = None
    game_repository = None

    def setUp(self):
        self.pgsql = testing.postgresql.Postgresql()
        self.conn = psycopg2.connect(**self.pgsql.dsn())
        self.game_repository = GameRepository(self.conn)

    def tearDown(self):
        self.conn.close()
        self.pgsql.stop()

    # =========================
    # Test insert game function
    # =========================
    def test_insert_game_new_game(self):
        with closing(self.conn.cursor()) as cursor:
            cursor.execute("CREATE TABLE games(id serial, language varchar(40), game_status int, active boolean, user_id int, score int)")
            response = self.game_repository.insert_game(1, 'NL', 5)

        self.assertEqual(response, 1)

    # ========================================
    # Test validate game function with user_id
    # ========================================
    def test_validate_game_user_id(self):
        with closing(self.conn.cursor()) as cursor:
            cursor.execute("CREATE TABLE games(id serial, language varchar(40), game_status int, active boolean, user_id int, score int)")
            cursor.execute("INSERT INTO games VALUES (1, 'NL', 5, True, 1, 0)")
            response = self.game_repository._validate_game(1)

        self.assertEqual(response, True)

    # ========================================
    # Test validate game function with game_id
    # ========================================
    def test_validate_game_game_id(self):
        with closing(self.conn.cursor()) as cursor:
            cursor.execute("CREATE TABLE games(id serial, language varchar(40), game_status int, active boolean, user_id int, score int)")
            cursor.execute("INSERT INTO games VALUES (1, 'NL', 5, True, 1, 0)")
            response = self.game_repository._validate_game_game_id(1)

        self.assertEqual(response, True)

    # ===============================
    # Test get game round information
    # ===============================
    def test_get_game_round_information(self):
        with closing(self.conn.cursor()) as cursor:
            # Create tables
            cursor.execute("CREATE TABLE games(id serial, language varchar(40), game_status int, active boolean, user_id int, score int)")
            cursor.execute("CREATE TABLE rounds(id serial, active boolean, word varchar(7), game_id int)")
            cursor.execute("CREATE TABLE turns(id serial, guessed_word varchar(7), started_at date, round_id int)")

            # Create data
            cursor.execute("INSERT INTO games VALUES (1, 'NL', 5, True, 1, 0)")
            cursor.execute("INSERT INTO rounds VALUES (1, True, 'PIZZA', 1)")
            cursor.execute("INSERT INTO turns VALUES (1, NULL, now()::timestamptz, 1)")
            response = self.game_repository.get_game_round_information(1)

        self.assertEqual(response.__eq__({'game_id': 1, 'game_language': 'NL', 'word_length': 5, 'correct_word': 'PIZZA',
                                          'round_id': 1, 'turn_start_time': datetime.datetime.now().date()}), True)

    # =========================
    # Test get game information
    # =========================
    def test_get_game_information(self):
        with closing(self.conn.cursor()) as cursor:
            # Create tables
            cursor.execute("CREATE TABLE games(id serial, language varchar(40), game_status int, active boolean, user_id int, score int)")

            # Create data
            cursor.execute("INSERT INTO games VALUES (1, 'NL', 5, True, 1, 0)")
            response = self.game_repository.get_game_information(1)

        self.assertEqual(response.__eq__({'game_id': 1, 'word_length': 5, 'language': 'NL'}), True)

    # ============================
    # Test update game word length
    # ============================
    def test_update_game_word_new_word_length(self):
        with closing(self.conn.cursor()) as cursor:
            # Create tables
            cursor.execute(
                "CREATE TABLE games(id serial, language varchar(40), game_status int, active boolean, user_id int, score int)")

            # Create data
            cursor.execute("INSERT INTO games VALUES (1, 'NL', 5, True, 1, 0)")
            self.game_repository.update_game_word_length(1, 6)

        self.assertEqual(True, True)

    # ======================
    # Test update game score
    # ======================
    def test_update_game_score_plus_one(self):
        with closing(self.conn.cursor()) as cursor:
            # Create tables
            cursor.execute(
                "CREATE TABLE games(id serial, language varchar(40), game_status int, active boolean, user_id int, score int)")

            # Create data
            cursor.execute("INSERT INTO games VALUES (1, 'NL', 5, True, 1, 0)")
            self.game_repository.update_game_score(1)

        self.assertEqual(True, True)

    # ======================
    # Test end game function
    # ======================
    def test_end_game_function(self):
        with closing(self.conn.cursor()) as cursor:
            # Create tables
            cursor.execute(
                "CREATE TABLE games(id serial, language varchar(40), game_status int, active boolean, user_id int, score int)")

            # Create data
            cursor.execute("INSERT INTO games VALUES (1, 'NL', 5, True, 1, 0)")
            self.game_repository.update_end_game(1)

        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
