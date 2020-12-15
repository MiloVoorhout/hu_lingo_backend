"""
    This script initializes a single instance of a database connection.
"""

# pylint: disable=import-error
import os
import psycopg2


class DatabaseConnection:
    """
    :type connection: connection instance
    """
    connection = None

    @staticmethod
    def get_connection(_self):
        """Returns instance of database connection

        :param _self: class instance
        :return: instance of connection
        """
        if _self.connection is None:
            _self.connection = psycopg2.connect(
                host=os.environ.get("DB_HOST"),
                database=os.environ.get("DB_NAME"),
                user=os.environ.get("DB_USER"),
                password=os.environ.get("DB_PASS"),
                port=os.environ.get("DB_PORT")
            )

        return _self.connection

    @staticmethod
    def close_connection(_self):
        """Closes the database connection

        :param _self: class instance
        :return: void
        """
        print('Closing connection.\n')
        if _self.connection is not None:
            _self.connection.close()
            _self.connection = None
