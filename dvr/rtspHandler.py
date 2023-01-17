import cv2
from loguru import logger
from PyQt5.QtGui import QPixmap, QImage

from threading import Thread

class CaptureIpCameraFramesWorker:
    def __init__(self, url, the_disp):
        self.url = url
        self.active = False
        self.fps = 0
        self.disp = the_disp
        self.thread = None

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
        cap = cv2.VideoCapture(self.url)
        self.fps = cap.get(cv2.CAP_PROP_FPS)
        if not cap.isOpened():
            logger.error(f"Opening {self.url} is failed!")
            self.active = False
            cap.release()
            return
        logger.trace(f"Opening {self.url} is successful!")
        while self.active:
            ret, frame = cap.read()
            if not ret:
                break
            cv_rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            cv_rgb_image = self.prepare_disp_img(cv_rgb_image, self.disp.width(), self.disp.height())
            qt_rgb_image_scaled = self.convert_nparray_to_QImage(cv_rgb_image)
            self.disp.setPixmap(QPixmap.fromImage(qt_rgb_image_scaled))
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
    RTSP_URL1 = 'rtsp://admin:YSBCAW@192.168.100.2:554/H.264'
    RTSP_URL2 = "rtsp://admin:YICSVF@192.168.100.3:554/H.264"
    RTSP_URL3 = "rtsp://admin:PEJEEL@192.168.100.4:554/H.264"

    cap = cv2.VideoCapture(RTSP_URL3)#, cv2.CAP_FFMPEG)

    if not cap.isOpened():
        print('Cannot open RTSP stream')
        exit(-1)

    while True:
        _, frame = cap.read()
        cv2.imshow('RTSP stream', frame)

        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()