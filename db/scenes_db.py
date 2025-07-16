from db.database import Database
from db.logging import logger


class Scenes:
    def __init__(self, db: Database):
        self.db = db

    def create_scene(self, game_id: int, title: str = None):
        try:
            self.db.cursor.execute(
                """
                INSERT INTO scenes (game_id, title)
                VALUES (%s, %s)
                RETURNING id;
                """,
                (game_id, title)
            )
            scene_id = self.db.cursor.fetchone()['id']
            self.db.conn.commit()
            logger.info(f"Scene created: {scene_id} in game {game_id}")
            return scene_id
        except Exception as e:
            logger.error(f"Error creating scene for game {game_id}: {e}")
            self.db.conn.rollback()

    def get_scene_by_id(self, scene_id: int):
        try:
            self.db.cursor.execute("SELECT * FROM scenes WHERE id = %s;", (scene_id,))
            scene = self.db.cursor.fetchone()
            logger.info(f"Fetched scene by id: {scene_id}")
            return scene
        except Exception as e:
            logger.error(f"Error fetching scene {scene_id}: {e}")

    def get_scenes_by_game(self, game_id: int):
        try:
            self.db.cursor.execute("SELECT * FROM scenes WHERE game_id = %s;", (game_id,))
            scenes = self.db.cursor.fetchall()
            logger.info(f"Fetched {len(scenes)} scenes for game {game_id}")
            return scenes
        except Exception as e:
            logger.error(f"Error fetching scenes for game {game_id}: {e}")

    def update_scene_title(self, scene_id: int, new_title: str):
        try:
            self.db.cursor.execute(
                "UPDATE scenes SET title = %s WHERE id = %s;",
                (new_title, scene_id)
            )
            self.db.conn.commit()
            logger.info(f"Updated scene {scene_id} title to '{new_title}'")
            return True
        except Exception as e:
            logger.error(f"Error updating title of scene {scene_id}: {e}")
            self.db.conn.rollback()

    def delete_scene(self, scene_id: int):
        try:
            self.db.cursor.execute("DELETE FROM scenes WHERE id = %s;", (scene_id,))
            self.db.conn.commit()
            logger.info(f"Deleted scene {scene_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting scene {scene_id}: {e}")
            self.db.conn.rollback()
