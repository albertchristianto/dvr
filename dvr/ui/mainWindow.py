from PyQt5.QtWidgets import QMainWindow, QSizePolicy, QScrollArea, QLabel
from PyQt5.QtGui import QPixmap, QImage, QPalette
from PyQt5.QtCore import QEvent, QObject
from PyQt5 import QtCore
from loguru import logger
import cv2
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

        # Dictionary to keep the state of a camera. The camera state will be: Normal or Maximized.
        # self.list_of_cameras_state = {}

        # Create an instance of a QLabel class to show camera 1.
        self.Ch1.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.Ch1.setScaledContents(True)
        self.Ch1.installEventFilter(self)
        self.Ch1.setObjectName("Ch1")
        # self.list_of_cameras_state["Ch1"] = "Normal"

        # # Create an instance of a QScrollArea class to scroll camera 1 image.
        # self.QScrollArea_1 = QScrollArea()
        # self.QScrollArea_1.setBackgroundRole(QPalette.Dark)
        # self.QScrollArea_1.setWidgetResizable(True)
        # self.QScrollArea_1.setWidget(self.Ch1)

        # Create an instance of a QLabel class to show camera 2.
        self.Ch2.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.Ch2.setScaledContents(True)
        self.Ch2.installEventFilter(self)
        self.Ch2.setObjectName("Ch2")
        # self.list_of_cameras_state["Ch2"] = "Normal"

        # # Create an instance of a QScrollArea class to scroll camera 2 image.
        # self.QScrollArea_2 = QScrollArea()
        # self.QScrollArea_2.setBackgroundRole(QPalette.Dark)
        # self.QScrollArea_2.setWidgetResizable(True)
        # self.QScrollArea_2.setWidget(self.Ch2)

        # Create an instance of a QLabel class to show camera 3.
        self.Ch3.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.Ch3.setScaledContents(True)
        self.Ch3.installEventFilter(self)
        self.Ch3.setObjectName("Ch3")
        # self.list_of_cameras_state["Ch3"] = "Normal"

        # # Create an instance of a QScrollArea class to scroll camera 3 image.
        # self.QScrollArea_3 = QScrollArea()
        # self.QScrollArea_3.setBackgroundRole(QPalette.Dark)
        # self.QScrollArea_3.setWidgetResizable(True)
        # self.QScrollArea_3.setWidget(self.Ch3)

        # Create an instance of a QLabel class to show camera 4.
        self.Ch4.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.Ch4.setScaledContents(True)
        self.Ch4.installEventFilter(self)
        self.Ch4.setObjectName("Ch4")
        # self.list_of_cameras_state["Ch4"] = "Normal"

        # # Create an instance of a QScrollArea class to scroll camera 4 image.
        # self.QScrollArea_4 = QScrollArea()
        # self.QScrollArea_4.setBackgroundRole(QPalette.Dark)
        # self.QScrollArea_4.setWidgetResizable(True)
        # self.QScrollArea_4.setWidget(self.Ch4)

        # Set the UI elements for this Widget class.
        self.__SetupUI()

        # Create an instance of CaptureIpCameraFramesWorker.
        if self.SystemParam['Ch1'][0] != "":
            # logger.trace(f"Opening {self.SystemParam['Ch1'][0]}")
            self.CaptureIpCameraFramesWorker_1 = CaptureIpCameraFramesWorker(self.SystemParam['Ch1'][0], self.Ch1)
            # self.CaptureIpCameraFramesWorker_1.ImageUpdated.connect(lambda image: self.ShowCamera1(image))
        if self.SystemParam['Ch2'][0] != "":
            # logger.trace(f"Opening {self.SystemParam['Ch2'][0]}")
            self.CaptureIpCameraFramesWorker_2 = CaptureIpCameraFramesWorker(self.SystemParam['Ch2'][0], self.Ch2)
            # self.CaptureIpCameraFramesWorker_2.ImageUpdated.connect(lambda image: self.ShowCamera2(image))
        if self.SystemParam['Ch3'][0] != "":
            # logger.trace(f"Opening {self.SystemParam['Ch3'][0]}")
            self.CaptureIpCameraFramesWorker_3 = CaptureIpCameraFramesWorker(self.SystemParam['Ch3'][0], self.Ch3)
            # self.CaptureIpCameraFramesWorker_3.ImageUpdated.connect(lambda image: self.ShowCamera3(image))
        if self.SystemParam['Ch4'][0] != "":
            # logger.trace(f"Opening {self.SystemParam['Ch4'][0]}")
            self.CaptureIpCameraFramesWorker_4 = CaptureIpCameraFramesWorker(self.SystemParam['Ch4'][0], self.Ch4)
            # self.CaptureIpCameraFramesWorker_4.ImageUpdated.connect(lambda image: self.ShowCamera4(image))
        if self.SystemParam['Ch1'][0] != "":
            self.CaptureIpCameraFramesWorker_1.start()
        if self.SystemParam['Ch2'][0] != "":
            self.CaptureIpCameraFramesWorker_2.start()
        if self.SystemParam['Ch3'][0] != "":
            self.CaptureIpCameraFramesWorker_3.start()
        if self.SystemParam['Ch4'][0] != "":
            self.CaptureIpCameraFramesWorker_4.start()

    def __SetupUI(self) -> None:
        self.CentralWidget.setLayout(self.MainLayout)
        self.setCentralWidget(self.CentralWidget)# Set the central widget.
        self.setMinimumSize(800, 600)
        self.showMaximized()
        self.setStyleSheet("QMainWindow {background: 'black';}")
        self.setWindowTitle("IP Camera System")

    # @QtCore.pyqtSlot()
    # def ShowCamera1(self, frame: QImage) -> None:
    #     # logger.trace("ch1 updated!")
    #     self.Ch1.setPixmap(QPixmap.fromImage(frame))

    # @QtCore.pyqtSlot()
    # def ShowCamera2(self, frame: QImage) -> None:
    #     # logger.trace("ch2 updated!")
    #     self.Ch2.setPixmap(QPixmap.fromImage(frame))

    # @QtCore.pyqtSlot()
    # def ShowCamera3(self, frame: QImage) -> None:
    #     # logger.trace("ch3 updated!")
    #     self.Ch3.setPixmap(QPixmap.fromImage(frame))

    # @QtCore.pyqtSlot()
    # def ShowCamera4(self, frame: QImage) -> None:
    #     # logger.trace("ch4 updated!")
    #     self.Ch4.setPixmap(QPixmap.fromImage(frame))

    # # Override method for class MainWindow.
    # def eventFilter(self, source: QObject, event: QEvent) -> bool:
    #     """
    #     Method to capture the events for objects with an event filter installed.
    #     :param source: The object for whom an event took place.
    #     :param event: The event that took place.
    #     :return: True if event is handled.
    #     """
    #     #
    #     if event.type() == QtCore.QEvent.MouseButtonDblClick:
    #         if source.objectName() == 'Ch1':
    #             #
    #             if self.list_of_cameras_state["Ch1"] == "Normal":
    #                 self.QScrollArea_2.hide()
    #                 self.QScrollArea_3.hide()
    #                 self.QScrollArea_4.hide()
    #                 self.list_of_cameras_state["Ch1"] = "Maximized"
    #             else:
    #                 self.QScrollArea_2.show()
    #                 self.QScrollArea_3.show()
    #                 self.QScrollArea_4.show()
    #                 self.list_of_cameras_state["Ch1"] = "Normal"
    #         elif source.objectName() == 'Ch2':
    #             #
    #             if self.list_of_cameras_state["Ch2"] == "Normal":
    #                 self.QScrollArea_1.hide()
    #                 self.QScrollArea_3.hide()
    #                 self.QScrollArea_4.hide()
    #                 self.list_of_cameras_state["Ch2"] = "Maximized"
    #             else:
    #                 self.QScrollArea_1.show()
    #                 self.QScrollArea_3.show()
    #                 self.QScrollArea_4.show()
    #                 self.list_of_cameras_state["Ch2"] = "Normal"
    #         elif source.objectName() == 'Ch3':
    #             #
    #             if self.list_of_cameras_state["Ch3"] == "Normal":
    #                 self.QScrollArea_1.hide()
    #                 self.QScrollArea_2.hide()
    #                 self.QScrollArea_4.hide()
    #                 self.list_of_cameras_state["Ch3"] = "Maximized"
    #             else:
    #                 self.QScrollArea_1.show()
    #                 self.QScrollArea_2.show()
    #                 self.QScrollArea_4.show()
    #                 self.list_of_cameras_state["Ch3"] = "Normal"
    #         elif source.objectName() == 'Ch4':
    #             #
    #             if self.list_of_cameras_state["Ch4"] == "Normal":
    #                 self.QScrollArea_1.hide()
    #                 self.QScrollArea_2.hide()
    #                 self.QScrollArea_3.hide()
    #                 self.list_of_cameras_state["Ch4"] = "Maximized"
    #             else:
    #                 self.QScrollArea_1.show()
    #                 self.QScrollArea_2.show()
    #                 self.QScrollArea_3.show()
    #                 self.list_of_cameras_state["Ch4"] = "Normal"
    #         else:
    #             return super(MainWindow, self).eventFilter(source, event)
    #         return True
    #     else:
    #         return super(MainWindow, self).eventFilter(source, event)

    # # Overwrite method closeEvent from class QMainWindow.
    # def closeEvent(self, event) -> None:
    #     # If thread getIpCameraFrameWorker_1 is running, then exit it.
    #     if self.CaptureIpCameraFramesWorker_1.isRunning():
    #         self.CaptureIpCameraFramesWorker_1.quit()
    #     # If thread getIpCameraFrameWorker_2 is running, then exit it.
    #     if self.CaptureIpCameraFramesWorker_2.isRunning():
    #         self.CaptureIpCameraFramesWorker_2.quit()
    #     # If thread getIpCameraFrameWorker_3 is running, then exit it.
    #     if self.CaptureIpCameraFramesWorker_3.isRunning():
    #         self.CaptureIpCameraFramesWorker_3.quit()
    #     # Accept the event
    #     event.accept()