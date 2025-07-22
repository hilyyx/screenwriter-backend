import psycopg2
from psycopg2.extras import RealDictCursor
import json
import logging
import os
from dotenv import load_dotenv
from urllib.parse import urlparse


load_dotenv()


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    filename='db.log',
    filemode='a'
)

class Database:
    def __init__(self):
        self.dbres = os.getenv('DATABASE_URL')
        self.dbname = os.getenv('DB_NAME')
        self.user = os.getenv('DB_USER')
        self.password = os.getenv('DB_PASSWORD')
        self.host = os.getenv('DB_HOST')
        self.port = int(os.getenv('DB_PORT'))

        try:
            self.db_params = urlparse(self.dbres)
            self.conn = psycopg2.connect(
                self.dbres,
                sslmode = "require"
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