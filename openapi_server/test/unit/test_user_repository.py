import unittest
from contextlib import closing
import psycopg2
import testing.postgresql
from passlib.handlers.sha2_crypt import sha256_crypt

from openapi_server.core.application.user.user_logic import UserService
from openapi_server.core.port.data.user.user_repository import UserRepository


class TestUserRepository(unittest.TestCase):

    def setUp(self) -> None:
        self.pgsql = testing.postgresql.Postgresql()
        self.conn = psycopg2.connect(**self.pgsql.dsn())
        self.user_service = UserService(UserRepository(self.conn))

    def tearDown(self):
        self.conn.close()
        self.pgsql.stop()

    # ===============
    # Test user login
    # ===============
    def test_user_login(self):
        with closing(self.conn.cursor()) as cursor:
            cursor.execute("CREATE TABLE users(id serial, username varchar(40), password varchar(255))")
            cursor.execute("INSERT INTO users VALUES (1, 'tester', %s)", [sha256_crypt.hash('testing')])
            response = self.user_service.check_user_login('tester', 'testing')
        self.assertEqual(response, 1)


if __name__ == '__main__':
    unittest.main()
