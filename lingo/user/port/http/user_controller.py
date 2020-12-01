"""
    This controller contains all functions of user
"""

# pylint: disable=import-error
import json
from flask import make_response
from psycopg2.extras import RealDictCursor
from lingo.extentions.database_singleton import DatabaseConnection


def get_users():
    """
    Get all users
    :return: all users
    """
    con = DatabaseConnection.get_connection(DatabaseConnection)
    cur = con.cursor(cursor_factory=RealDictCursor)
    cur.execute("select * from users")
    results = json.dumps(cur.fetchall())
    cur.close()
    print(results)

    return make_response(results, 200)
