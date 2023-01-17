from PyQt5.QtWidgets import QMainWindow, QSizePolicy, QApplication
from PyQt5.QtCore import QTimer
from loguru import logger
import numpy as np
import json

from .template import Ui_MainWindow
from ..rtspHandler import CaptureIpCameraFramesWorker

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        f = open('app.cfg')
        self.SystemParam = json.load(f)

        self.Ch1.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.Ch1.setScaledContents(True)
        self.Ch1.installEventFilter(self)
        self.Ch1.setObjectName(self.SystemParam['Ch1'][1])

        self.Ch2.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.Ch2.setScaledContents(True)
        self.Ch2.installEventFilter(self)
        self.Ch2.setObjectName(self.SystemParam['Ch2'][1])

        self.Ch3.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.Ch3.setScaledContents(True)
        self.Ch3.installEventFilter(self)
        self.Ch3.setObjectName(self.SystemParam['Ch3'][1])

        self.Ch4.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.Ch4.setScaledContents(True)
        self.Ch4.installEventFilter(self)
        self.Ch4.setObjectName(self.SystemParam['Ch4'][1])

        self.startQThread()
        self.__SetupUI()# Set the UI elements for this Widget class.
        self.timer = QTimer()
        self.timer.timeout.connect(self.watchQThread)
        self.timer.start(1000)

    def startQThread(self):
        if self.SystemParam['Ch1'][0] != "":
            # logger.trace(f"Opening {self.SystemParam['Ch1'][0]}")
            self.CaptureIpCameraFramesWorker_1 = CaptureIpCameraFramesWorker(self.SystemParam['Ch1'][0], self.Ch1)
            logger.trace("Starting Channel 1 thread!")
            self.CaptureIpCameraFramesWorker_1.start()
        if self.SystemParam['Ch2'][0] != "":
            # logger.trace(f"Opening {self.SystemParam['Ch2'][0]}")
            self.CaptureIpCameraFramesWorker_2 = CaptureIpCameraFramesWorker(self.SystemParam['Ch2'][0], self.Ch2)
            logger.trace("Starting Channel 2 thread!")
            self.CaptureIpCameraFramesWorker_2.start()
        if self.SystemParam['Ch3'][0] != "":
            # logger.trace(f"Opening {self.SystemParam['Ch3'][0]}")
            self.CaptureIpCameraFramesWorker_3 = CaptureIpCameraFramesWorker(self.SystemParam['Ch3'][0], self.Ch3)
            logger.trace("Starting Channel 3 thread!")
            self.CaptureIpCameraFramesWorker_3.start()
        if self.SystemParam['Ch4'][0] != "":
            # logger.trace(f"Opening {self.SystemParam['Ch4'][0]}")
            self.CaptureIpCameraFramesWorker_4 = CaptureIpCameraFramesWorker(self.SystemParam['Ch4'][0], self.Ch4)
            logger.trace("Starting Channel 4 thread!")
            self.CaptureIpCameraFramesWorker_4.start()

    def watchQThread(self):
        if self.CaptureIpCameraFramesWorker_1 is not None and not self.CaptureIpCameraFramesWorker_1.isRunning():
            logger.trace("Re-Starting Channel 1 thread!")
            self.CaptureIpCameraFramesWorker_1.start()
        if self.CaptureIpCameraFramesWorker_2 is not None and not self.CaptureIpCameraFramesWorker_2.isRunning():
            logger.trace("Re-Starting Channel 2 thread!")
            self.CaptureIpCameraFramesWorker_2.start()
        if self.CaptureIpCameraFramesWorker_3 is not None and not self.CaptureIpCameraFramesWorker_3.isRunning():
            logger.trace("Re-Starting Channel 3 thread!")
            self.CaptureIpCameraFramesWorker_3.start()
        if self.CaptureIpCameraFramesWorker_4 is not None and not self.CaptureIpCameraFramesWorker_4.isRunning():
            logger.trace("Re-Starting Channel 4 thread!")
            self.CaptureIpCameraFramesWorker_4.start()
        # QApplication.processEvents()

    def closeEvent(self):
        print("User has clicked the red x on the main window")
        if self.CaptureIpCameraFramesWorker_1 is not None:
            self.CaptureIpCameraFramesWorker_1.stop()
        if self.CaptureIpCameraFramesWorker_2 is not None:
            self.CaptureIpCameraFramesWorker_2.stop()
        if self.CaptureIpCameraFramesWorker_3 is not None:
            self.CaptureIpCameraFramesWorker_3.stop()
        if self.CaptureIpCameraFramesWorker_4 is not None:
            self.CaptureIpCameraFramesWorker_4.stop()
        logger.trace("Quit!")

    def __SetupUI(self) -> None:
        self.CentralWidget.setLayout(self.MainLayout)
        self.setCentralWidget(self.CentralWidget)# Set the central widget.
        # self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, False)
        self.setMinimumSize(800, 600)
        self.showMaximized()
        self.setStyleSheet("QMainWindow {background: 'black';}")
        self.setWindowTitle("IP Camera System")
        self.CaptureIpCameraFramesWorker_1 = None
        self.CaptureIpCameraFramesWorker_2 = None
        self.CaptureIpCameraFramesWorker_3 = None
        self.CaptureIpCameraFramesWorker_4 = None