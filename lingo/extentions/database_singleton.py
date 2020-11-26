import os
import psycopg2
from configparser import ConfigParser

config_object = ConfigParser()
config_object.read("credentials/config.ini")

database_info = config_object["DATABASE"]


class DatabaseConnection:
    """
    :type connection: connection instance
    """
    connection = None
    cursor = None

    @staticmethod
    def get_connection(_self):
        """Returns instance of database connection

        :param _self: class instance
        :return: instance of connection
        """
        if _self.connection is None:
            _self.connection = psycopg2.connect(
                host=database_info["DB_HOST"],
                database=database_info["DB_NAME"],
                user=database_info["DB_USER"],
                password=database_info["DB_PASS"],
                port=database_info["DB_PORT"]
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