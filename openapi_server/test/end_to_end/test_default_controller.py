# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_guess_word(self):
        """Test case for guess_word

        Make a guess of the correct word
        """
        query_string = [('guessed_word', HELLO)]
        headers = { 
            'Accept': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/api/game/turn',
            method='POST',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_lingo_auth_auth_check_token(self):
        """Test case for lingo_auth_auth_check_token

        Return secret string
        """
        headers = { 
            'Authorization': 'Bearer special-key',
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
        query_string = [('username', Username),
                        ('password', Password)]
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

    def test_lingo_auth_auth_get_secret(self):
        """Test case for lingo_auth_auth_get_secret

        Return secret string
        """
        headers = { 
            'Accept': 'text/plain',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/api/secret',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_lingo_game_port_http_game_controller_create_game_controller(self):
        """Test case for lingo_game_port_http_game_controller_create_game_controller

        Start a game
        """
        headers = { 
            'Accept': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/api/game',
            method='POST',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_lingo_game_port_http_game_controller_create_round_controller(self):
        """Test case for lingo_game_port_http_game_controller_create_round_controller

        Start a round
        """
        headers = { 
            'Accept': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/api/game/round',
            method='POST',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_lingo_user_port_http_user_controller_get_users(self):
        """Test case for lingo_user_port_http_user_controller_get_users

        
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/api/user/all',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
