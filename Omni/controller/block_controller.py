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

    def update_block(self, block):
        logging.info(f'Updating block: {block.title}')
        self.db.update_block(block)

    def delete_block(self, block):
        logging.info(f'Deleting block: {block.title}')
        self.db.delete_block(block)

    def complete_block(self, block):
        logging.info(f'Completing block: {block.title}')
        self.db.complete_block(block)

    def search_blocks(self, text):
        logging.info(f'Searching blocks with text: {text}')
        return self.db.search_blocks(text)
