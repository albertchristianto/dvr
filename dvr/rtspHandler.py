import cv2
from loguru import logger
from PyQt5.QtGui import QImage
from PyQt5.QtCore import pyqtSignal, QObject

from threading import Thread

class CaptureIpCameraFramesWorker(QObject):
    # Signal emitted when a new image or a new frame is ready.
    ImageUpdated = pyqtSignal(QImage)
    def __init__(self, url, disp):
        super(CaptureIpCameraFramesWorker, self).__init__()
        self.url = url
        self.active = False
        self.fps = 0
        self.thread = None
        self.disp = disp

    def start(self):
        self.active = True
        self.thread = Thread(target=self.run)
        self.thread.start()

    def stop(self):
        self.active = False
        if self.thread is not None:
            self.thread.join()

    def isRunning(self):
        return self.active

    def run(self):
        cap = cv2.VideoCapture(self.url, cv2.CAP_FFMPEG)
        while not cap.isOpened():
            logger.error(f"Trying {self.url} again")
            cap = cv2.VideoCapture(self.url, cv2.CAP_FFMPEG)
            if not self.active:
                return
        self.fps = cap.get(cv2.CAP_PROP_FPS)
        logger.trace(f"Opening {self.url} is successful!")
        while self.active:
            ret, frame = cap.read()
            if not ret:
                logger.trace(f"Broken {self.url}!")
                break
            cv_rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            cv_rgb_image = self.prepare_disp_img(cv_rgb_image, self.disp.width(), self.disp.height())
            qt_rgb_image_scaled = self.convert_nparray_to_QImage(cv_rgb_image)
            self.ImageUpdated.emit(qt_rgb_image_scaled)
            # self.disp.setPixmap(QPixmap.fromImage(qt_rgb_image_scaled))
        self.active = False
        cap.release()

    def prepare_disp_img(self, img, w, h):
        disp = img.copy()
        if disp.ndim == 1:
            disp =  cv2.cvtColor(disp, cv2.COLOR_GRAY2RGB)
        # w, h = self.InputImage.width(), self.InputImage.height()
        disp = cv2.resize(disp, (w, h), interpolation = cv2.INTER_AREA)
        return disp

    def convert_nparray_to_QImage(self, disp):
        h, w, c = disp.shape
        qimg = QImage(disp.data, w, h, (3 * w), QImage.Format_RGB888) 
        return qimg


if __name__ == "__main__":
    RTSP_URL1 = 'rtsp://admin:YSBCAW@192.168.100.2:554/Streaming/Channels/101'
    RTSP_URL2 = "rtsp://admin:YICSVF@192.168.100.3:554/Streaming/Channels/101"
    RTSP_URL3 = "rtsp://admin:PEJEEL@192.168.100.4:554//Streaming/Channels/101"
    RTSP_URL4 = "rtsp://admin:BYBOQZ@192.168.100.5:554/Streaming/Channels/101"

    cap = cv2.VideoCapture(RTSP_URL2)#, cv2.CAP_FFMPEG)

    if not cap.isOpened():
        print('Cannot open RTSP stream')
        exit(-1)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("there is no frame!!")
            break
        cv2.imshow('RTSP stream', frame)

        if cv2.waitKey(1) == 27:
            print("exit")
            break

    print("Done!")
    cap.release()
    cv2.destroyAllWindows()