from db.database import Database
from db.logging import logger
import json

class Dialogues:
    def __init__(self, db: Database):
        self.db = db

    def create_dialogue(self, scene_id: int, title: str, data):
        try:
            self.db.cursor.execute(
                """
                INSERT INTO dialogues (scene_id, title, data)
                VALUES (%s, %s, %s)
                RETURNING id;
                """,
                (scene_id, title, json.dumps(data))
            )
            dialogue_id = self.db.cursor.fetchone()["id"]
            self.db.conn.commit()
            logger.info(f"Dialogue created: {dialogue_id} in scene {scene_id}")
            return dialogue_id
        except Exception as e:
            logger.error(f"Error creating dialogue for scene {scene_id}: {e}")
            self.db.conn.rollback()

    def get_dialogue_by_id(self, dialogue_id: int):
        try:
            self.db.cursor.execute("SELECT * FROM dialogues WHERE id = %s;", (dialogue_id,))
            dialogue = self.db.cursor.fetchone()
            logger.info(f"Fetched dialogue by id: {dialogue_id}")
            return dialogue
        except Exception as e:
            logger.error(f"Error fetching dialogue {dialogue_id}: {e}")

    def get_dialogues_by_scene(self, scene_id: int):
        try:
            self.db.cursor.execute("SELECT * FROM dialogues WHERE scene_id = %s;", (scene_id,))
            dialogues = self.db.cursor.fetchall()
            logger.info(f"Fetched {len(dialogues)} dialogues for scene {scene_id}")
            return dialogues
        except Exception as e:
            logger.error(f"Error fetching dialogues for scene {scene_id}: {e}")

    def update_dialogue_data(self, dialogue_id: int, new_data):
        try:
            self.db.cursor.execute(
                "UPDATE dialogues SET data = %s WHERE id = %s;",
                (json.dumps(new_data), dialogue_id)
            )
            self.db.conn.commit()
            logger.info(f"Updated data of dialogue {dialogue_id}")
            return True
        except Exception as e:
            logger.error(f"Error updating data for dialogue {dialogue_id}: {e}")
            self.db.conn.rollback()

    def update_dialogue_title(self, dialogue_id: int, new_title: str):
        try:
            self.db.cursor.execute(
                "UPDATE dialogues SET title = %s WHERE id = %s;",
                (new_title, dialogue_id)
            )
            self.db.conn.commit()
            logger.info(f"Updated title of dialogue {dialogue_id} to '{new_title}'")
            return True
        except Exception as e:
            logger.error(f"Error updating title for dialogue {dialogue_id}: {e}")
            self.db.conn.rollback()

    def delete_dialogue(self, dialogue_id: int):
        try:
            self.db.cursor.execute("DELETE FROM dialogues WHERE id = %s;", (dialogue_id,))
            self.db.conn.commit()
            logger.info(f"Deleted dialogue {dialogue_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting dialogue {dialogue_id}: {e}")
            self.db.conn.rollback()
