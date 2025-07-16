from db.database import Database
from db.logging import logger

class Games:
    def __init__(self, db: Database):
        self.db = db

    def create_game(self):
        self.db.cursor.execute()