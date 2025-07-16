from db.database import Database
from db.logging import logger

class Characters:
    def __init__(self, db: Database):
        self.db = db

    def create_character(self, game_id: int, is_npc: bool, name: str, profession: str, goal: str,
                         talk_style: str, traits: str, appearance: str, dialogue_id: int = None):
        try:
            self.db.cursor.execute(
                """
                INSERT INTO characters (
                    game_id, dialogue_id, is_npc, name, profession,
                    goal, talk_style, traits, appearance
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id;
                """,
                (game_id, dialogue_id, is_npc, name, profession, goal, talk_style, traits, appearance)
            )
            character_id = self.db.cursor.fetchone()["id"]
            self.db.conn.commit()
            logger.info(f"Character created: {character_id} ({name}) in game {game_id}")
            return character_id
        except Exception as e:
            logger.error(f"Error creating character for game {game_id}: {e}")
            self.db.conn.rollback()

    def get_character_by_id(self, character_id: int):
        try:
            self.db.cursor.execute("SELECT * FROM characters WHERE id = %s;", (character_id,))
            character = self.db.cursor.fetchone()
            logger.info(f"Fetched character by id: {character_id}")
            return character
        except Exception as e:
            logger.error(f"Error fetching character {character_id}: {e}")

    def get_characters_by_game(self, game_id: int):
        try:
            self.db.cursor.execute("SELECT * FROM characters WHERE game_id = %s;", (game_id,))
            characters = self.db.cursor.fetchall()
            logger.info(f"Fetched {len(characters)} characters for game {game_id}")
            return characters
        except Exception as e:
            logger.error(f"Error fetching characters for game {game_id}: {e}")

    def get_characters_by_dialogue(self, dialogue_id: int):
        try:
            self.db.cursor.execute("SELECT * FROM characters WHERE dialogue_id = %s;", (dialogue_id,))
            characters = self.db.cursor.fetchall()
            logger.info(f"Fetched {len(characters)} characters for dialogue {dialogue_id}")
            return characters
        except Exception as e:
            logger.error(f"Error fetching characters for dialogue {dialogue_id}: {e}")

    def update_character(self, character_id: int, **kwargs):
        try:
            fields = []
            values = []
            for key, value in kwargs.items():
                fields.append(f"{key} = %s")
                values.append(value)
            values.append(character_id)
            set_clause = ", ".join(fields)
            query = f"UPDATE characters SET {set_clause} WHERE id = %s;"
            self.db.cursor.execute(query, tuple(values))
            self.db.conn.commit()
            logger.info(f"Updated character {character_id} fields: {list(kwargs.keys())}")
            return True
        except Exception as e:
            logger.error(f"Error updating character {character_id}: {e}")
            self.db.conn.rollback()

    def delete_character(self, character_id: int):
        try:
            self.db.cursor.execute("DELETE FROM characters WHERE id = %s;", (character_id,))
            self.db.conn.commit()
            logger.info(f"Deleted character {character_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting character {character_id}: {e}")
            self.db.conn.rollback()
