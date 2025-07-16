from db.database import Database
from db.logging import logger
import json

class Users:
    def __init__(self, db: Database):
        self.db = db

    def create_user(self, mail: str, name: str, surname: str, password_hash: str, data: dict = None):
        if data is None:
            data = {"games": []}
        try:
            self.db.cursor.execute(
                """
                INSERT INTO users (mail, name, surname, password_hash, data)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id;
                """,
                (mail, name, surname, password_hash, json.dumps(data))
            )
            user_id = self.db.cursor.fetchone()["id"]
            self.db.conn.commit()
            logger.info(f"The user has been created: {user_id} ({name})")
            return user_id
        except Exception as e:
            logger.error(f"Error when creating user {name}: {e}")
            self.db.conn.rollback()

    def get_user_by_mail(self, mail: str):
        try:
            self.db.cursor.execute("SELECT * FROM users WHERE mail = %s;", (mail,))
            user = self.db.cursor.fetchone()
            logger.info(f"Received user by mail: {mail}")
            return user
        except Exception as e:
            logger.error(f"Error when receiving user by mail {mail}: {e}")

    def get_user_by_id(self, user_id: int):
        try:
            self.db.cursor.execute("SELECT * FROM users WHERE id = %s;", (user_id,))
            user = self.db.cursor.fetchone()
            logger.info(f"Received user by id: {user_id}")
            return user
        except Exception as e:
            logger.error(f"Error when receiving user by id {user_id}: {e}")

    def get_user_data(self, user_id: int):
        try:
            self.db.cursor.execute("SELECT data FROM users WHERE id = %s;", (user_id,))
            row = self.db.cursor.fetchone()
            logger.info(f"Received data for user {user_id}")
            return row["data"] if row else None
        except Exception as e:
            logger.error(f"Error when receiving data for user {user_id}: {e}")

    def update_user_data(self, user_id: int, new_data: dict):
        try:
            self.db.cursor.execute(
                "UPDATE users SET data = %s WHERE id = %s;",
                (json.dumps(new_data), user_id)
            )
            self.db.conn.commit()
            logger.info(f"Updated data for user {user_id}")
            return True
        except Exception as e:
            logger.error(f"Error updating data for user {user_id}: {e}")
            self.db.conn.rollback()

    def update_user_name(self, user_id: int, new_name: str, new_surname: str):
        try:
            self.db.cursor.execute(
                "UPDATE users SET name = %s, surname = %s WHERE id = %s;",
                (new_name, new_surname, user_id)
            )
            self.db.conn.commit()
            logger.info(f"User name {user_id} updated ")
            return True
        except Exception as e:
            logger.error(f"Error updating user name {user_id}: {e}")
            self.db.conn.rollback()

    def update_user_password(self, user_id: int, new_pass: str):
        try:
            self.db.cursor.execute(
                "UPDATE users SET password_hash = %s WHERE id = %s;",
                (new_pass, user_id)
            )
            self.db.conn.commit()
            logger.info(f"Password updated for user {user_id}")
            return True
        except Exception as e:
            logger.error(f"Error updating password for user {user_id}: {e}")
            self.db.conn.rollback()

    def delete_user(self, user_id: int):
        try:
            self.db.cursor.execute("DELETE FROM users WHERE id = %s;", (user_id,))
            self.db.conn.commit()
            logger.info(f"User {user_id} deleted")
            return True
        except Exception as e:
            logger.error(f"Error deleting user {user_id}: {e}")
            self.db.conn.rollback()
