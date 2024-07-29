import logging
from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow
import sys

def main():
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info('Starting Timetune application...')
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
