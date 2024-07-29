from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QCalendarWidget, QVBoxLayout, QWidget, QPushButton, QListView, QAbstractItemView, QLineEdit
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt, QTimer
from controller.block_controller import BlockController
from ui.block_dialog import BlockDialog
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), 'main_window.ui'), self)
        self.controller = BlockController()
        self.model = QStandardItemModel(self.block_list)
        self.block_list.setModel(self.model)
        self.block_list.setSelectionMode(QAbstractItemView.SingleSelection)
        
        self.add_block_button.clicked.connect(self.open_add_block_dialog)
        self.edit_block_button.clicked.connect(self.edit_selected_block)
        self.delete_block_button.clicked.connect(self.delete_selected_block)
        self.complete_block_button.clicked.connect(self.complete_selected_block)
        self.theme_button.clicked.connect(self.toggle_theme)
        self.search_bar.textChanged.connect(self.search_blocks)
        
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
        selected_indexes = self.block_list.selectedIndexes()
        if selected_indexes:
            selected_item = self.model.itemFromIndex(selected_indexes[0])
            block = selected_item.data()
            dialog = BlockDialog(self, block)
            if dialog.exec_():
                updated_block = dialog.get_block()
                self.controller.update_block(updated_block)
                self.refresh_block_list()

    def delete_selected_block(self):
        selected_indexes = self.block_list.selectedIndexes()
        if selected_indexes:
            selected_item = self.model.itemFromIndex(selected_indexes[0])
            block = selected_item.data()
            self.controller.delete_block(block)
            self.refresh_block_list()

    def complete_selected_block(self):
        selected_indexes = self.block_list.selectedIndexes()
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
        with open(os.path.join(os.path.dirname(__file__), '../resources/styles.qss'), 'r') as file:
            self.setStyleSheet(file.read())
