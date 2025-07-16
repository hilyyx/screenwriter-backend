from db.database import Database
from db.logging import logger


class Games:
    def __init__(self, db: Database):
        self.db = db

    def create_game(self, user_id: int, title: str, technology_level: str = None, magic: str = None):
        try:
            self.db.cursor.execute(
                """
                INSERT INTO games (user_id, title, technology_level, magic)
                VALUES (%s, %s, %s, %s)
                RETURNING id;
                """,
                (user_id, title, technology_level, magic)
            )
            game_id = self.db.cursor.fetchone()["id"]
            self.db.conn.commit()
            logger.info(f"Game created: {game_id} by user {user_id}")
            return game_id
        except Exception as e:
            logger.error(f"Error creating game for user {user_id}: {e}")
            self.db.conn.rollback()

    def get_game_by_id(self, game_id: int):
        try:
            self.db.cursor.execute("SELECT * FROM games WHERE id = %s;", (game_id,))
            game = self.db.cursor.fetchone()
            logger.info(f"Fetched game by id: {game_id}")
            return game
        except Exception as e:
            logger.error(f"Error fetching game {game_id}: {e}")

    def get_games_by_user(self, user_id: int):
        try:
            self.db.cursor.execute("SELECT * FROM games WHERE user_id = %s;", (user_id,))
            games = self.db.cursor.fetchall()
            logger.info(f"Fetched {len(games)} games for user {user_id}")
            return games
        except Exception as e:
            logger.error(f"Error fetching games for user {user_id}: {e}")

    def search_games_by_title(self, title: str):
        try:
            self.db.cursor.execute(
                "SELECT * FROM games WHERE title = %s;", (title,))
            new_title = self.db.cursor.fetchall()
            logger.info(f"Found {len(new_title)} games matching title part: '{title}'")
            return new_title
        except Exception as e:
            logger.error(f"Error searching games by title '{title}': {e}")

    def update_game_title(self, game_id: int, new_title: str):
        try:
            self.db.cursor.execute(
                "UPDATE games SET title = %s WHERE id = %s;",
                (new_title, game_id)
            )
            self.db.conn.commit()
            logger.info(f"Updated title of game {game_id} to '{new_title}'")
            return True
        except Exception as e:
            logger.error(f"Error updating title for game {game_id}: {e}")
            self.db.conn.rollback()

    def update_game_settings(self, game_id: int, technology_level: str = None, magic: str = None):
        try:
            self.db.cursor.execute(
                "UPDATE games SET technology_level = %s, magic = %s WHERE id = %s;",
                (technology_level, magic, game_id)
            )
            self.db.conn.commit()
            logger.info(f"Updated settings of game {game_id}")
            return True
        except Exception as e:
            logger.error(f"Error updating settings for game {game_id}: {e}")
            self.db.conn.rollback()

    def delete_game(self, game_id: int):
        try:
            self.db.cursor.execute("DELETE FROM games WHERE id = %s;", (game_id,))
            self.db.conn.commit()
            logger.info(f"Deleted game {game_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting game {game_id}: {e}")
            self.db.conn.rollback()
