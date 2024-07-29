# utils/export.py
import csv
from model.database import Database

class Exporter:
    def __init__(self):
        self.db = Database()

    def export_to_csv(self, filename):
        blocks = self.db.get_all_blocks()
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['Title', 'Start Time', 'End Time', 'Color', 'Description']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for block in blocks:
                writer.writerow({
                    'Title': block.title,
                    'Start Time': block.start_time,
                    'End Time': block.end_time,
                    'Color': block.color,
                    'Description': block.description
                })
