import unittest
from contextlib import closing

from openapi_server.core.port.data.auth.user_repository import get_user_id_login


class TestUserRepository(unittest.TestCase):
    # ===============
    # Test user login
    # ===============
    def test_user_login(self):
        response = get_user_id_login('tester', 'testing')
        self.assertEqual(response, 1)


if __name__ == '__main__':
    unittest.main()
