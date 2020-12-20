import unittest
from contextlib import closing

from openapi_server.core.application.user.user_logic import UserService
from openapi_server.core.port.data.user.user_repository import UserRepository
from openapi_server.extentions.database_singleton import DatabaseConnection


class TestUserRepository(unittest.TestCase):

    def setUp(self) -> None:
        self.user_service = UserService(UserRepository(DatabaseConnection.get_connection(DatabaseConnection())))

    # ===============
    # Test user login
    # ===============
    def test_user_login(self):
        response = self.user_service.check_user_login('tester', 'testing')
        self.assertEqual(response, 1)


if __name__ == '__main__':
    unittest.main()
