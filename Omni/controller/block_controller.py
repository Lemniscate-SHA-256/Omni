import logging
from model.database import Database
from model.block import Block

class BlockController:
    def __init__(self):
        logging.info('Initializing BlockController...')
        self.db = Database()

    def add_block(self, block):
        logging.info(f'Adding block: {block.title}')
        self.db.insert_block(block)
    
    def get_all_blocks(self):
        logging.info('Fetching all blocks...')
        return self.db.get_all_blocks()
