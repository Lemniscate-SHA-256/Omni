from PyQt5.QtWidgets import QMainWindow, QCalendarWidget, QVBoxLayout, QWidget, QPushButton, QListView, QAbstractItemView
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from controller.block_controller import BlockController
from ui.block_dialog import BlockDialog
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.controller = BlockController()
        self.model = QStandardItemModel(self.block_list)
        self.block_list.setModel(self.model)
        self.refresh_block_list()

    def init_ui(self):
        self.setWindowTitle('Timetune')
        self.setGeometry(100, 100, 800, 600)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()

        self.calendar = QCalendarWidget()
        layout.addWidget(self.calendar)
        
        self.block_list = QListView()
        self.block_list.setSelectionMode(QAbstractItemView.SingleSelection)
        layout.addWidget(self.block_list)

        add_block_button = QPushButton('Add Block')
        add_block_button.clicked.connect(self.open_add_block_dialog)
        layout.addWidget(add_block_button)

        central_widget.setLayout(layout)
        self.load_stylesheet()
        self.show()

    def open_add_block_dialog(self):
        dialog = BlockDialog(self)
        if dialog.exec_():
            block = dialog.get_block()
            self.controller.add_block(block)
            self.refresh_block_list()

    def refresh_block_list(self):
        blocks = self.controller.get_all_blocks()
        self.model.clear()
        for block in blocks:
            item = QStandardItem(f'{block.title}: {block.start_time} - {block.end_time}')
            item.setData(block)
            item.setEditable(False)
            self.model.appendRow(item)

    def load_stylesheet(self):
        with open('resources/styles.qss', 'r') as file:
            self.setStyleSheet(file.read())
