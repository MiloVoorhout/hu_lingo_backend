# coding: utf-8
from __future__ import absolute_import
import unittest
from contextlib import closing

from openapi_server.core.port.http.auth.auth import generate_token
from openapi_server.extentions.database_singleton import DatabaseConnection
from openapi_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def setUp(self) -> None:
        self.bearerToken = 'Bearer ' + (generate_token('tester', 'testing')).data.decode('utf-8')
        self.conn = DatabaseConnection.get_connection(DatabaseConnection())

    def tearDown(self) -> None:
        self.conn.close()

    def test_lingo_auth_auth_check_token(self):
        """Test case for lingo_auth_auth_check_token

        Return secret string
        """
        headers = { 
            'Authorization': self.bearerToken,
        }
        response = self.client.open(
            '/api/token/validate',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_lingo_auth_auth_generate_token(self):
        """Test case for lingo_auth_auth_generate_token

        Return JWT token
        """
        query_string = [('username', 'tester'),
                        ('password', 'testing')]
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/auth',
            method='POST',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_lingo_game_port_http_game_controller_create_game_controller(self):
        """Test case for lingo_game_port_http_game_controller_create_game_controller

        Start a game
        """
        # Clear test data in the database
        with closing(self.conn.cursor()) as cursor:
            cursor.execute("DELETE FROM public.games WHERE user_id = 1;")
            self.conn.commit()

        # The controller test
        query_string = [('language', 'NL')]
        headers = {
            'Accept': 'application/json',
            'Authorization': self.bearerToken,
        }
        response = self.client.open(
            '/api/game',
            method='POST',
            headers=headers,
            query_string=query_string
        )
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_guess_word(self):
        """Test case for guess_word
        Make a guess of the correct word
        """
        # Clear test data in the database and create fake data
        with closing(self.conn.cursor()) as cursor:
            cursor.execute("DELETE FROM public.games WHERE user_id = 1;")
            cursor.execute(
                "INSERT INTO public.games(id, language, game_status, active, user_id, score) VALUES (69, 'NL', 5, True, 1, 0);"
            )
            cursor.execute(
                "INSERT INTO public.rounds(id, active, word, game_id) VALUES (13, True, 'BAARD', 69)"
            )
            cursor.execute(
                "INSERT INTO public.turns(id, guessed_word, started_at, round_id) VALUES (33, NULL, now()::timestamptz, 13)"
            )
            self.conn.commit()

        query_string = [('guessed_word', 'DRAAD')]
        headers = {
            'Accept': 'application/json',
            'Authorization': self.bearerToken,
        }
        response = self.client.open(
            '/api/game/turn',
            method='POST',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_lingo_game_port_http_game_controller_create_round_controller(self):
        """Test case for lingo_game_port_http_game_controller_create_round_controller

        Start a round
        """
        # Clear test data in the database and create fake data
        with closing(self.conn.cursor()) as cursor:
            cursor.execute("DELETE FROM public.games WHERE user_id = 1;")
            cursor.execute("INSERT INTO public.games(language, game_status, active, user_id, score) VALUES ('NL', 6, True, 1, 0);")
            self.conn.commit()

        headers = {
            'Accept': 'application/json',
            'Authorization': self.bearerToken,
        }
        response = self.client.open(
            '/api/game/round',
            method='POST',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_lingo_user_port_http_user_controller_get_high_score(self):
        """Test case for lingo_port_http_user_controller_get_high_score

        Get users high scores
        """
        headers = {
            'Accept': 'application/json',
            'Authorization': self.bearerToken,
        }
        response = self.client.open(
            '/api/highscore',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_lingo_user_port_http_user_create_new_user(self):
        """Test case for lingo_port_http_user_controller_create_new_user

        Create a new user
        """
        query_string = [('username', 'apitesting'),
                        ('password', 'testing')]
        headers = {
            'Accept': 'application/json',
            'Authorization': self.bearerToken,
        }
        response = self.client.open(
            '/api/user',
            method='POST',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

        # Clear test data in the database and create fake data
        with closing(self.conn.cursor()) as cursor:
            cursor.execute("DELETE FROM public.users WHERE username = 'apitesting';")
            self.conn.commit()


if __name__ == '__main__':
    unittest.main()
