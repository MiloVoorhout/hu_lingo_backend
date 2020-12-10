# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.test import BaseTestCase


class TestAliveController(BaseTestCase):
    """AliveController integration test stubs"""

    def test_is_alive(self):
        """Test case for is_alive

        Api keepalive
        """
        headers = { 
        }
        response = self.client.open(
            '/api/ping',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
