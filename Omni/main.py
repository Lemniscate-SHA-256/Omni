import logging
from PyQt5.QtWidgets import QApplication
from ui.ui_main_window import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QTimer
from controller.block_controller import BlockController
from ui.block_dialog import BlockDialog
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QAbstractItemView
import sys

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.controller = BlockController()
        self.model = QStandardItemModel(self.blockListView)
        self.blockListView.setModel(self.model)
        self.blockListView.setSelectionMode(QAbstractItemView.SingleSelection)
        
        self.addBlockButton.clicked.connect(self.open_add_block_dialog)
        self.editBlockButton.clicked.connect(self.edit_selected_block)
        self.deleteBlockButton.clicked.connect(self.delete_selected_block)
        self.completeBlockButton.clicked.connect(self.complete_selected_block)
        self.themeButton.clicked.connect(self.toggle_theme)
        self.searchBar.textChanged.connect(self.search_blocks)
        
        self.refresh_block_list()
        self.load_stylesheet()
        self.show()

        # Timer for notifications
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_notifications)
        self.timer.start(60000)  # Check every minute

    def open_add_block_dialog(self):
        dialog = BlockDialog(self)
        if dialog.exec_():
            block = dialog.get_block()
            self.controller.add_block(block)
            self.refresh_block_list()

    def edit_selected_block(self):
        selected_indexes = self.blockListView.selectedIndexes()
        if selected_indexes:
            selected_item = self.model.itemFromIndex(selected_indexes[0])
            block = selected_item.data()
            dialog = BlockDialog(self, block)
            if dialog.exec_():
                updated_block = dialog.get_block()
                self.controller.update_block(updated_block)
                self.refresh_block_list()

    def delete_selected_block(self):
        selected_indexes = self.blockListView.selectedIndexes()
        if selected_indexes:
            selected_item = self.model.itemFromIndex(selected_indexes[0])
            block = selected_item.data()
            self.controller.delete_block(block)
            self.refresh_block_list()

    def complete_selected_block(self):
        selected_indexes = self.blockListView.selectedIndexes()
        if selected_indexes:
            selected_item = self.model.itemFromIndex(selected_indexes[0])
            block = selected_item.data()
            self.controller.complete_block(block)
            self.refresh_block_list()

    def search_blocks(self, text):
        blocks = self.controller.search_blocks(text)
        self.model.clear()
        for block in blocks:
            item = QStandardItem(f'{block.title}: {block.start_time} - {block.end_time}')
            item.setData(block)
            item.setEditable(False)
            self.model.appendRow(item)

    def refresh_block_list(self):
        blocks = self.controller.get_all_blocks()
        self.model.clear()
        for block in blocks:
            item = QStandardItem(f'{block.title}: {block.start_time} - {block.end_time}')
            item.setData(block)
            item.setEditable(False)
            self.model.appendRow(item)

    def toggle_theme(self):
        # Implement theme toggling logic
        pass

    def check_notifications(self):
        # Implement notification checking logic
        pass

    def load_stylesheet(self):
        with open('resources/styles.qss', 'r') as file:
            self.setStyleSheet(file.read())

def main():
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info('Starting Timetune application...')
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
