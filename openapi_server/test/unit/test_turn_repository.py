import unittest
from contextlib import closing
import psycopg2
import testing.postgresql

from openapi_server.core.port.data.game.round_repository import RoundRepository
from openapi_server.core.port.data.game.turn_repository import TurnRepository


class TestTurnRepository(unittest.TestCase):
    def setUp(self):
        self.pgsql = testing.postgresql.Postgresql()
        self.conn = psycopg2.connect(**self.pgsql.dsn())
        self.turn_repository = TurnRepository(RoundRepository(self.conn), self.conn)

    def tearDown(self):
        self.conn.close()
        self.pgsql.stop()

    # =========================
    # Test insert turn function
    # =========================
    def test_insert_turn_new_turn(self):
        with closing(self.conn.cursor()) as cursor:
            # Create tables
            cursor.execute("CREATE TABLE rounds(id serial, active boolean, word varchar(7), game_id int)")
            cursor.execute("CREATE TABLE turns(id serial, guessed_word varchar(7), started_at date, round_id int)")

            # Insert data
            cursor.execute("INSERT INTO rounds VALUES (1, True, 'BOOMER', 1)")
            response = self.turn_repository.insert_turn(1)

        self.assertEqual(response, True)

    # ================
    # Test update turn
    # ================
    def test_update_turn(self):
        with closing(self.conn.cursor()) as cursor:
            # Create tables
            cursor.execute("CREATE TABLE turns(id serial, guessed_word varchar(7), started_at date, round_id int)")
            cursor.execute("CREATE TABLE rounds(id serial, active boolean, word varchar(7), game_id int)")

            # Insert data
            cursor.execute("INSERT INTO rounds VALUES (1, True, 'BOOMER', 1)")
            cursor.execute("INSERT INTO turns VALUES (1, NULL, now()::timestamptz, 1)")
            self.turn_repository.update_turn('BOOMER', 1)

        self.assertEqual(True, True)

    # =========================
    # Test count turns function
    # =========================
    def test_count_turns(self):
        with closing(self.conn.cursor()) as cursor:
            # Create tables
            cursor.execute("CREATE TABLE turns(id serial, guessed_word varchar(7), started_at date, round_id int)")
            cursor.execute("CREATE TABLE rounds(id serial, active boolean, word varchar(7), game_id int)")

            # Insert data
            cursor.execute("INSERT INTO rounds VALUES (1, True, 'BOOMER', 1)")
            cursor.execute("INSERT INTO turns VALUES (1, 'BOOMER', now()::timestamptz, 1)")
            cursor.execute("INSERT INTO turns VALUES (2, 'PIZZA', now()::timestamptz, 1)")
            cursor.execute("INSERT INTO turns VALUES (3, 'TESTING', now()::timestamptz, 1)")

            response = self.turn_repository.get_turn_count(1)

        self.assertEqual(response, 3)


if __name__ == '__main__':
    unittest.main()
