"""
    This repository contains all functions connecting to the database table User
"""

# pylint: disable=import-error
import psycopg2
from flask import abort
from openapi_server.extentions.database_singleton import DatabaseConnection

# Singleton database connection
conn = DatabaseConnection.get_connection(DatabaseConnection())


# pylint: disable=inconsistent-return-statements
def get_user_id_login(username, password):
    """
    Check if user exists
    :param username: user name identifier
    :param password: user password
    :return: user_id
    """
    try:
        curs = conn.cursor()
        curs.execute(
            "SELECT id FROM users WHERE username = %s AND password = %s",
            (username, password))
        user_id = curs.fetchone()[0]
        conn.commit()  # <- MUST commit to reflect the inserted data
        curs.close()   # <- Always close an cursor

        return user_id
    except psycopg2.OperationalError as error:
        abort(500, {'message': error})
# pylint: enable=inconsistent-return-statements
