import sqlite3
import logging
from model.block import Block

class Database:
    def __init__(self, db_name='timetune.db'):
        logging.info(f'Connecting to database {db_name}...')
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        logging.info('Creating blocks table if not exists...')
        query = '''CREATE TABLE IF NOT EXISTS blocks (
                    id INTEGER PRIMARY KEY,
                    title TEXT,
                    start_time TEXT,
                    end_time TEXT,
                    color TEXT,
                    description TEXT)'''
        self.conn.execute(query)
        self.conn.commit()

    def insert_block(self, block):
        logging.info(f'Inserting block into database: {block.title}')
        query = '''INSERT INTO blocks (title, start_time, end_time, color, description)
                   VALUES (?, ?, ?, ?, ?)'''
        self.conn.execute(query, (block.title, block.start_time, block.end_time, block.color, block.description))
        self.conn.commit()

    def get_all_blocks(self):
        logging.info('Fetching all blocks from database...')
        cursor = self.conn.cursor()
        cursor.execute("SELECT title, start_time, end_time, color, description FROM blocks")
        blocks = cursor.fetchall()
        return [Block(*block) for block in blocks]
