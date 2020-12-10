# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.test import BaseTestCase


class TestWordController(BaseTestCase):
    """WordController integration test stubs"""

    def test_lingo_game_application_game_logic_choose_random_word(self):
        """Test case for lingo_game_application_game_logic_choose_random_word

        Get a random word based on word length
        """
        headers = { 
        }
        response = self.client.open(
            '/api/choose/{word_length}'.format(word_length=56),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
