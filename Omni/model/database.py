import sqlite3
import logging
from model.block import Block

class Database:
    def __init__(self, db_name='timetune.db'):
        logging.info(f'Connecting to database {db_name}...')
        self.conn = sqlite3.connect(db_name)
        self.create_table()
        self.update_table_schema()

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

    def update_table_schema(self):
        logging.info('Updating table schema if necessary...')
        cursor = self.conn.cursor()
        cursor.execute("PRAGMA table_info(blocks)")
        columns = [column[1] for column in cursor.fetchall()]
        if 'completed' not in columns:
            logging.info('Adding completed column to blocks table...')
            cursor.execute("ALTER TABLE blocks ADD COLUMN completed INTEGER DEFAULT 0")
            self.conn.commit()

    def insert_block(self, block):
        logging.info(f'Inserting block into database: {block.title}')
        query = '''INSERT INTO blocks (title, start_time, end_time, color, description, completed)
                   VALUES (?, ?, ?, ?, ?, 0)'''
        self.conn.execute(query, (block.title, block.start_time, block.end_time, block.color, block.description))
        self.conn.commit()

    def get_all_blocks(self):
        logging.info('Fetching all blocks from database...')
        cursor = self.conn.cursor()
        cursor.execute("SELECT title, start_time, end_time, color, description FROM blocks WHERE completed=0")
        blocks = cursor.fetchall()
        return [Block(*block) for block in blocks]

    def update_block(self, block):
        logging.info(f'Updating block in database: {block.title}')
        query = '''UPDATE blocks SET title=?, start_time=?, end_time=?, color=?, description=? WHERE id=?'''
        self.conn.execute(query, (block.title, block.start_time, block.end_time, block.color, block.description, block.id))
        self.conn.commit()

    def delete_block(self, block):
        logging.info(f'Deleting block from database: {block.title}')
        query = '''DELETE FROM blocks WHERE id=?'''
        self.conn.execute(query, (block.id,))
        self.conn.commit()

    def complete_block(self, block):
        logging.info(f'Marking block as completed in database: {block.title}')
        query = '''UPDATE blocks SET completed=1 WHERE id=?'''
        self.conn.execute(query, (block.id,))
        self.conn.commit()

    def search_blocks(self, text):
        logging.info(f'Searching blocks in database with text: {text}')
        cursor = self.conn.cursor()
        query = "SELECT title, start_time, end_time, color, description FROM blocks WHERE completed=0 AND (title LIKE ? OR description LIKE ?)"
        cursor.execute(query, (f'%{text}%', f'%{text}%'))
        blocks = cursor.fetchall()
        return [Block(*block) for block in blocks]
