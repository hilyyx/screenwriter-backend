import psycopg2
from psycopg2.extras import RealDictCursor
import json
import logging
import os
from dotenv import load_dotenv


load_dotenv()


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    filename='db.log',
    filemode='a'
)

class Database:
    def __init__(self):
        self.dbname = os.getenv('DB_NAME')
        self.user = os.getenv('DB_USER')
        self.password = os.getenv('DB_PASSWORD')
        self.host = os.getenv('DB_HOST')
        self.port = int(os.getenv('DB_PORT'))

        try:
            self.conn = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)
            logging.info(f"Connection to the database is successful: {self.host}:{self.port}/{self.dbname}")
        except Exception as e:
            logging.error(f"Error connecting to the database: {e}")
            raise

    def close(self):
        try:
            self.cursor.close()
            self.conn.close()
            logging.info("The database connection is closed")
        except Exception as e:
            logging.error(f"Error closing the connection: {e}")
'''
    # ---------- GAMES ----------
    def create_game(self, user_id, title, technology_level=None, magic=None):
        try:
            self.cursor.execute(
                """INSERT INTO games (user_id, title, technology_level, magic)
                   VALUES (%s, %s, %s, %s) RETURNING id;""",
                (user_id, title, technology_level, magic)
            )
            game_id = self.cursor.fetchone()['id']
            self.conn.commit()
            logging.info(f"The game was created by: {game_id} ({title}) for the user {user_id}")
            return game_id
        except Exception as e:
            logging.error(f"Error when creating the game: {e}")

    def get_games_by_user(self, user_id):
        try:
            self.cursor.execute("SELECT * FROM games WHERE user_id = %s;", (user_id,))
            games = self.cursor.fetchall()
            logging.info(f"User's games have been received {user_id}: {len(games)} шт.")
            return games
        except Exception as e:
            logging.error(f"Error when receiving user's games {user_id}: {e}")

    def update_game_title(self, game_id, new_title):
        try:
            self.cursor.execute(
                "UPDATE games SET title = %s WHERE id = %s;", (new_title, game_id)
            )
            self.conn.commit()
            logging.info(f"The name of the game {game_id} has been updated to '{new_title}'")
        except Exception as e:
            logging.error(f"Error updating the game name {game_id}: {e}")

    def delete_game(self, game_id):
        try:
            self.cursor.execute("DELETE FROM games WHERE id = %s;", (game_id,))
            self.conn.commit()
            logging.info(f"Game deleted: {game_id}")
        except Exception as e:
            logging.error(f"Error deleting the game {game_id}: {e}")

    # ---------- SCENES ----------
    def create_scene(self, game_id, title):
        try:
            self.cursor.execute(
                """INSERT INTO scenes (game_id, title)
                   VALUES (%s, %s) RETURNING id;""",
                (game_id, title)
            )
            scene_id = self.cursor.fetchone()['id']
            self.conn.commit()
            logging.info(f"The scene was created: {scene_id} for the game {game_id}")
            return scene_id
        except Exception as e:
            logging.error(f"Error when creating the scene: {e}")

    def update_scene_title(self, scene_id, new_title):
        try:
            self.cursor.execute(
                "UPDATE scenes SET title = %s WHERE id = %s;", (new_title, scene_id)
            )
            self.conn.commit()
            logging.info(f"The name of the scene {scene_id} has been updated to '{new_title}'")
        except Exception as e:
            logging.error(f"Error updating the scene {scene_id}: {e}")

    def delete_scene(self, scene_id):
        try:
            self.cursor.execute("DELETE FROM scenes WHERE id = %s;", (scene_id,))
            self.conn.commit()
            logging.info(f"The scene has been deleted: {scene_id}")
        except Exception as e:
            logging.error(f"Error when deleting a scene  {scene_id}: {e}")

    # ---------- DIALOGUES ----------
    def create_dialogue(self, scene_id, title, data):
        try:
            self.cursor.execute(
                """INSERT INTO dialogues (scene_id, title, data)
                   VALUES (%s, %s, %s) RETURNING id;""",
                (scene_id, title, json.dumps(data))
            )
            dialogue_id = self.cursor.fetchone()['id']
            self.conn.commit()
            logging.info(f"Dialog created: {dialogue_id} for the scene {scene_id}")
            return dialogue_id
        except Exception as e:
            logging.error(f"Error when creating the dialog: {e}")

    def update_dialogue_data(self, dialogue_id, new_data):
        try:
            self.cursor.execute(
                "UPDATE dialogues SET data = %s WHERE id = %s;",
                (json.dumps(new_data), dialogue_id)
            )
            self.conn.commit()
            logging.info(f"Dialog data {dialogue_id} updated")
        except Exception as e:
            logging.error(f"Error updating dialog data {dialogue_id}: {e}")

    def delete_dialogue(self, dialogue_id):
        try:
            self.cursor.execute("DELETE FROM dialogues WHERE id = %s;", (dialogue_id,))
            self.conn.commit()
            logging.info(f"Dialog deleted: {dialogue_id}")
        except Exception as e:
            logging.error(f"Error deleting the dialog {dialogue_id}: {e}")

    # ---------- CHARACTERS ----------
    def create_character(self, game_id, is_npc, name, profession, goal,
                         talk_style, traits, appearance, dialogue_id=None):
        try:
            self.cursor.execute(
                """INSERT INTO characters (
                    game_id, dialogue_id, is_npc, name, profession,
                    goal, talk_style, traits, appearance
                   ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                   RETURNING id;""",
                (game_id, dialogue_id, is_npc, name, profession,
                 goal, talk_style, traits, appearance)
            )
            character_id = self.cursor.fetchone()['id']
            self.conn.commit()
            logging.info(f"The character is created: {character_id} ({name})")
            return character_id
        except Exception as e:
            logging.error(f"Error when creating a character: {e}")
'''
