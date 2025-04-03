import os

import mysql.connector
from model.User import User  # Assumes your User class is in user.py

class DBAccess:
    def __init__(self):
        self.config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'user': os.getenv('DB_USER', 'root'),
            'password': os.getenv('DB_PASSWORD', ''),
            'database': os.getenv('DB_NAME', 'LiveChat')
        }

    def get_user_by_username(self, username) -> User:
        conn = mysql.connector.connect(**self.config)
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute("SELECT * FROM Users WHERE username = %s", (username,))
            row = cursor.fetchone()
            if row:
                return User(
                    id=row['idUsers'],
                    username=row['username'],
                    password=row['password']
                )
        finally:
            cursor.close()
            conn.close()

        return None
