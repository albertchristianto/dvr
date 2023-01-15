import cv2
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QPixmap, QImage
from loguru import logger
import os 

class CaptureIpCameraFramesWorker(QThread):
    # Signal emitted when a new image or a new frame is ready.
    # ImageUpdated = pyqtSignal(QImage)

    def __init__(self, url, the_disp) -> None:
        super(CaptureIpCameraFramesWorker, self).__init__()
        # Declare and initialize instance variables.
        self.url = url
        self.__thread_active = True
        self.fps = 0
        self.__thread_pause = False
        self.disp = the_disp

    def run(self) -> None:
        # Capture video from a network stream.
        cap = cv2.VideoCapture(self.url)
        # Get default video FPS.
        self.fps = cap.get(cv2.CAP_PROP_FPS)
        # print(self.fps)
        # If video capturing has been initialized already.q
        if not cap.isOpened():
            logger.error(f"Opening {self.url} is failed!")
            # When everything done, release the video capture object.
            cap.release()
            # Tells the thread's event loop to exit with return code 0 (success).
            self.quit()
            return
        logger.trace(f"Opening {self.url} is successful!")
        # While the thread is active.
        while self.__thread_active:
            if self.__thread_pause:
                continue
            # Grabs, decodes and returns the next video frame.
            ret, frame = cap.read()
            # If frame is read correctly.
            if not ret:
                break
            # cv2.imshow(self.url, frame)
            # cv2.waitKey(1)
            cv_rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            cv_rgb_image = self.prepare_disp_img(cv_rgb_image, self.disp.width(), self.disp.height())
            qt_rgb_image_scaled = self.convert_nparray_to_QImage(cv_rgb_image)
            # Emit this signal to notify that a new image or frame is available.
            self.disp.setPixmap(QPixmap.fromImage(qt_rgb_image_scaled))
            # self.ImageUpdated.emit(qt_rgb_image_scaled)
            # logger.trace(f'{self.url} says hi!')
        # When everything done, release the video capture object.
        cap.release()
        # Tells the thread's event loop to exit with return code 0 (success).
        self.quit()

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

    def stop(self) -> None:
        self.__thread_active = False

    def pause(self) -> None:
        self.__thread_pause = True

    def unpause(self) -> None:
        self.__thread_pause = False

if __name__ == "__main__":
    RTSP_URL = 'rtsp://admin:YSBCAW@192.168.100.2:554/Streaming/Channels/101'

    cap = cv2.VideoCapture(RTSP_URL)#, cv2.CAP_FFMPEG)

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