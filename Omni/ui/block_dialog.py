from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QTimeEdit, QColorDialog, QTextEdit, QPushButton
from model.block import Block

class BlockDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Add/Edit Block')
        layout = QVBoxLayout()

        self.title_edit = QLineEdit()
        self.title_edit.setPlaceholderText('Title')
        layout.addWidget(self.title_edit)

        self.start_time_edit = QTimeEdit()
        layout.addWidget(self.start_time_edit)

        self.end_time_edit = QTimeEdit()
        layout.addWidget(self.end_time_edit)

        self.color_button = QPushButton('Select Color')
        self.color_button.clicked.connect(self.select_color)
        layout.addWidget(self.color_button)

        self.description_edit = QTextEdit()
        self.description_edit.setPlaceholderText('Description')
        layout.addWidget(self.description_edit)

        save_button = QPushButton('Save')
        save_button.clicked.connect(self.save_block)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def select_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.color = color.name()

    def save_block(self):
        self.block = Block(
            self.title_edit.text(),
            self.start_time_edit.time().toString('HH:mm'),
            self.end_time_edit.time().toString('HH:mm'),
            self.color,
            self.description_edit.toPlainText()
        )
        self.accept()

    def get_block(self):
        return self.block
