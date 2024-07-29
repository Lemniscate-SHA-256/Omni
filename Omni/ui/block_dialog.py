from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QColorDialog
from model.block import Block
import os

class BlockDialog(QDialog):
    def __init__(self, parent=None, block=None):
        super().__init__(parent)
        uic.loadUi(os.path.join(os.path.dirname(__file__), 'ui_block_dialog.ui'), self)
        self.color = None

        if block:
            self.titleEdit.setText(block.title)
            self.startTimeEdit.setTime(block.start_time)
            self.endTimeEdit.setTime(block.end_time)
            self.descriptionEdit.setPlainText(block.description)
            self.color = block.color

        self.colorButton.clicked.connect(self.select_color)
        self.saveButton.clicked.connect(self.save_block)

    def select_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.color = color.name()

    def save_block(self):
        self.block = Block(
            self.titleEdit.text(),
            self.startTimeEdit.time().toString('HH:mm'),
            self.endTimeEdit.time().toString('HH:mm'),
            self.color,
            self.descriptionEdit.toPlainText()
        )
        self.accept()

    def get_block(self):
        return self.block
