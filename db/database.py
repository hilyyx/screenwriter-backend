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