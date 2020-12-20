"""
    This repository contains all functions connecting to the database table User
"""

# pylint: disable=import-error
import psycopg2
from flask import abort


class UserRepository:
    """
    UserRepository class contains every round function that talks to the database
    """

    def __init__(self, database):
        self.conn = database

    # pylint: disable=inconsistent-return-statements
    def insert_user(self, username, password):
        """
        Insert a new user into user table
        :param username: users unique identifier
        :param password: encrypted password
        :return: Boolean
        """
        try:
            curs = self.conn.cursor()
            curs.execute("INSERT INTO users (username, password) "
                         "VALUES(%s, %s)",
                         (username, password))
            self.conn.commit()  # <- MUST commit to reflect the inserted data
            curs.close()  # <- Always close an cursor

            return True
        except psycopg2.OperationalError as error:
            self.conn.rollback()
            abort(500, {'message': error})

    # pylint: enable=inconsistent-return-statements

    # pylint: disable=inconsistent-return-statements
    def get_user_details(self, username):
        """
        Check if user exists
        :param username: user name identifier
        :return: user details
        """
        try:
            curs = self.conn.cursor()
            curs.execute(
                "SELECT id, password FROM users WHERE username = %s",
                [username])
            user_details = curs.fetchone()
            self.conn.commit()  # <- MUST commit to reflect the inserted data
            curs.close()  # <- Always close an cursor

            return {'user_id': user_details[0], 'password': user_details[1]}
        except psycopg2.OperationalError as error:
            abort(500, {'message': error})

    # pylint: enable=inconsistent-return-statements

    # pylint: disable=inconsistent-return-statements
    def get_high_scores(self, user_id):
        """
        Check if user exists
        :param user_id: user unique identifier
        :return: users high scores
        """
        try:
            curs = self.conn.cursor()
            curs.execute(
                "SELECT score, language FROM games WHERE user_id = %s",
                [user_id])
            rows = curs.fetchall()
            user_scores = []
            for row in rows:
                user_scores.append({row[1]: row[0]})
            curs.close()  # <- Always close an cursor

            return user_scores
        except psycopg2.OperationalError as error:
            abort(500, {'message': error})
    # pylint: enable=inconsistent-return-statements
