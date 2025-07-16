from db.database import Database
from db.logging import logger


class Users:
    def __init__(self, db: Database):
        self.db = db

    def create_user(self, mail, name, surname, password_hash):
        try:
            self.db.cursor.execute(
                """INSERT INTO users (mail, name, surname, password_hash)
                   VALUES (%s, %s, %s, %s) RETURNING id;""",
                (mail, name, surname, password_hash)
            )
            user_id = self.db.cursor.fetchone()['id']
            self.db.conn.commit()
            logger.info(f"The user has been created: {user_id} ({name})")
            return user_id
        except Exception as e:
            logger.error(f"Error when creating a user {name}: {e}")

    def get_user_by_mail(self, mail):
        try:
            self.db.cursor.execute("SELECT * FROM users WHERE mail = %s;", mail)
            user = self.db.cursor.fetchone()
            logger.info(f"Received a user with an email: {mail}")
            return user
        except Exception as e:
            logger.error(f"Error when receiving the user {mail}: {e}")

    def update_user_name(self, user_id, new_name):
        try:
            self.db.cursor.execute(
                "UPDATE users SET name = %s WHERE id = %s;", (new_name, user_id)
            )
            self.db.conn.commit()
            logger.info(f"User name {user_id} updated to {new_name}")
        except Exception as e:
            logger.error(f"Error updating the username {user_id}: {e}")

    def delete_user(self, user_id):
        try:
            self.db.cursor.execute("DELETE FROM users WHERE id = %s;", (user_id,))
            self.db.conn.commit()
            logger.info(f"The user has been deleted: {user_id}")
        except Exception as e:
            logger.error(f"Error when deleting a user {user_id}: {e}")
