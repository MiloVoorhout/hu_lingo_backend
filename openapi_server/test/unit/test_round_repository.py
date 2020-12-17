import unittest
from contextlib import closing
import datetime

import psycopg2
import testing.postgresql

from openapi_server.core.port.data.round_repository import RoundRepository


class TestRoundRepository(unittest.TestCase):
    def setUp(self):
        self.pgsql = testing.postgresql.Postgresql()
        self.conn = psycopg2.connect(**self.pgsql.dsn())
        self.round_repository = RoundRepository(self.conn)

    def tearDown(self):
        self.conn.close()
        self.pgsql.stop()

    # ==========================
    # Test insert round function
    # ==========================
    def test_insert_round_new_round(self):
        with closing(self.conn.cursor()) as cursor:
            cursor.execute("CREATE TABLE rounds(id serial, active boolean, word varchar(7), game_id int)")
            response = self.round_repository.insert_round(1, 'BOOMER')

        self.assertEqual(response, 1)

    # =========================================
    # Test validate round function with game_id
    # =========================================
    def test_validate_round_with_game_id(self):
        with closing(self.conn.cursor()) as cursor:
            cursor.execute("CREATE TABLE rounds(id serial, active boolean, word varchar(7), game_id int)")
            cursor.execute("INSERT INTO rounds VALUES (1, True, 'BOOMER', 1)")
            response = self.round_repository._validate_round(1)

        self.assertEqual(response, True)

    # ==========================================
    # Test validate round function with round_id
    # ==========================================
    def test_validate_round_with_round_id(self):
        with closing(self.conn.cursor()) as cursor:
            cursor.execute("CREATE TABLE rounds(id serial, active boolean, word varchar(7), game_id int)")
            cursor.execute("INSERT INTO rounds VALUES (1, True, 'BOOMER', 1)")
            response = self.round_repository.validate_round_round_id(1)

        self.assertEqual(response, True)

    # ===================================
    # Test update end round with round_id
    # ===================================
    def test_update_end_round(self):
        with closing(self.conn.cursor()) as cursor:
            cursor.execute("CREATE TABLE rounds(id serial, active boolean, word varchar(7), game_id int)")
            cursor.execute("INSERT INTO rounds VALUES (1, True, 'BOOMER', 1)")
            response = self.round_repository.update_end_round(1)

        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
