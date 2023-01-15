import sys

from PyQt5.QtWidgets import QApplication

from dvr.ui.mainWindow import MainWindow
from loguru import logger

LOG_LEVEL = 'TRACE'

logger.remove()
logger.add(sys.stdout, level=LOG_LEVEL)


app = QApplication(sys.argv)
win = MainWindow()
win.show()
sys.exit(app.exec())