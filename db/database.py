import psycopg2
from psycopg2.extras import RealDictCursor
import json
import logging
import os
from dotenv import load_dotenv


load_dotenv()

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    filename='db.log',
    filemode='a'
)

class Database:
    def __init__(self, dbname=None, user=None, password=None, host=None, port=None):
        self.dbname = dbname or os.getenv('DB_NAME', 'screenwriter_db')
        self.user = user or os.getenv('DB_USER', 'postgres')
        self.password = password or os.getenv('DB_PASSWORD', '')
        self.host = host or os.getenv('DB_HOST', 'localhost')
        self.port = port or int(os.getenv('DB_PORT', 5432))
        
        try:
            self.conn = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)
            logging.info(f"Подключение к базе данных успешно: {self.host}:{self.port}/{self.dbname}")
        except Exception as e:
            logging.error(f"Ошибка при подключении к БД: {e}")
            raise

    # ---------- USERS ----------
    def create_user(self, mail, name, surname, password_hash):
        try:
            self.cursor.execute(
                """INSERT INTO users (mail, name, surname, password_hash)
                   VALUES (%s, %s, %s, %s) RETURNING id;""",
                (mail, name, surname, password_hash)
            )
            user_id = self.cursor.fetchone()['id']
            self.conn.commit()
            logging.info(f"Пользователь создан: {user_id} ({name})")
            return user_id
        except Exception as e:
            logging.error(f"Ошибка при создании пользователя {name}: {e}")

    def get_user_by_name(self, name):
        try:
            self.cursor.execute("SELECT * FROM users WHERE name = %s;", (name,))
            user = self.cursor.fetchone()
            logging.info(f"Получен пользователь по имени: {name}")
            return user
        except Exception as e:
            logging.error(f"Ошибка при получении пользователя {name}: {e}")

    def update_user_name(self, user_id, new_name):
        try:
            self.cursor.execute(
                "UPDATE users SET name = %s WHERE id = %s;", (new_name, user_id)
            )
            self.conn.commit()
            logging.info(f"Имя пользователя {user_id} обновлено на {new_name}")
        except Exception as e:
            logging.error(f"Ошибка при обновлении имени пользователя {user_id}: {e}")

    def delete_user(self, user_id):
        try:
            self.cursor.execute("DELETE FROM users WHERE id = %s;", (user_id,))
            self.conn.commit()
            logging.info(f"Пользователь удалён: {user_id}")
        except Exception as e:
            logging.error(f"Ошибка при удалении пользователя {user_id}: {e}")

    def get_user_by_mail(self, mail):
        try:
            self.cursor.execute("SELECT * FROM users WHERE mail = %s;", (mail,))
            user = self.cursor.fetchone()
            logging.info(f"Получен пользователь с почтой: {mail}")
            return user
        except Exception as e:
            logging.error(f"Ошибка при получении пользователя {mail}: {e}")
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
            logging.info(f"Игра создана: {game_id} ({title}) для пользователя {user_id}")
            return game_id
        except Exception as e:
            logging.error(f"Ошибка при создании игры: {e}")

    def get_games_by_user(self, user_id):
        try:
            self.cursor.execute("SELECT * FROM games WHERE user_id = %s;", (user_id,))
            games = self.cursor.fetchall()
            logging.info(f"Получены игры пользователя {user_id}: {len(games)} шт.")
            return games
        except Exception as e:
            logging.error(f"Ошибка при получении игр пользователя {user_id}: {e}")

    def update_game_title(self, game_id, new_title):
        try:
            self.cursor.execute(
                "UPDATE games SET title = %s WHERE id = %s;", (new_title, game_id)
            )
            self.conn.commit()
            logging.info(f"Название игры {game_id} обновлено на '{new_title}'")
        except Exception as e:
            logging.error(f"Ошибка при обновлении названия игры {game_id}: {e}")

    def delete_game(self, game_id):
        try:
            self.cursor.execute("DELETE FROM games WHERE id = %s;", (game_id,))
            self.conn.commit()
            logging.info(f"Игра удалена: {game_id}")
        except Exception as e:
            logging.error(f"Ошибка при удалении игры {game_id}: {e}")

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
            logging.info(f"Сцена создана: {scene_id} для игры {game_id}")
            return scene_id
        except Exception as e:
            logging.error(f"Ошибка при создании сцены: {e}")

    def update_scene_title(self, scene_id, new_title):
        try:
            self.cursor.execute(
                "UPDATE scenes SET title = %s WHERE id = %s;", (new_title, scene_id)
            )
            self.conn.commit()
            logging.info(f"Название сцены {scene_id} обновлено на '{new_title}'")
        except Exception as e:
            logging.error(f"Ошибка при обновлении сцены {scene_id}: {e}")

    def delete_scene(self, scene_id):
        try:
            self.cursor.execute("DELETE FROM scenes WHERE id = %s;", (scene_id,))
            self.conn.commit()
            logging.info(f"Сцена удалена: {scene_id}")
        except Exception as e:
            logging.error(f"Ошибка при удалении сцены {scene_id}: {e}")

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
            logging.info(f"Диалог создан: {dialogue_id} для сцены {scene_id}")
            return dialogue_id
        except Exception as e:
            logging.error(f"Ошибка при создании диалога: {e}")

    def update_dialogue_data(self, dialogue_id, new_data):
        try:
            self.cursor.execute(
                "UPDATE dialogues SET data = %s WHERE id = %s;",
                (json.dumps(new_data), dialogue_id)
            )
            self.conn.commit()
            logging.info(f"Данные диалога {dialogue_id} обновлены")
        except Exception as e:
            logging.error(f"Ошибка при обновлении данных диалога {dialogue_id}: {e}")

    def delete_dialogue(self, dialogue_id):
        try:
            self.cursor.execute("DELETE FROM dialogues WHERE id = %s;", (dialogue_id,))
            self.conn.commit()
            logging.info(f"Диалог удалён: {dialogue_id}")
        except Exception as e:
            logging.error(f"Ошибка при удалении диалога {dialogue_id}: {e}")

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
            logging.info(f"Персонаж создан: {character_id} ({name})")
            return character_id
        except Exception as e:
            logging.error(f"Ошибка при создании персонажа: {e}")

    def update_character_goal(self, character_id, new_goal):
        try:
            self.cursor.execute(
                "UPDATE characters SET goal = %s WHERE id = %s;",
                (new_goal, character_id)
            )
            self.conn.commit()
            logging.info(f"Цель персонажа {character_id} обновлена")
        except Exception as e:
            logging.error(f"Ошибка при обновлении цели персонажа {character_id}: {e}")

    def delete_character(self, character_id):
        try:
            self.cursor.execute("DELETE FROM characters WHERE id = %s;", (character_id,))
            self.conn.commit()
            logging.info(f"Персонаж удалён: {character_id}")
        except Exception as e:
            logging.error(f"Ошибка при удалении персонажа {character_id}: {e}")

    # ---------- GENERAL ----------
    def close(self):
        try:
            self.cursor.close()
            self.conn.close()
            logging.info("Соединение с базой данных закрыто")
        except Exception as e:
            logging.error(f"Ошибка при закрытии соединения: {e}")
