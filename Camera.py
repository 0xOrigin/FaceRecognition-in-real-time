import os; os.environ["OPENCV_LOG_LEVEL"] = "SILENT"
import time
from threading import Thread
import cv2


class Camera:
    def __init__(self, camera_index=0):
        self.index = camera_index
        self.online = None
        self.frame = None
        self.__stopped = True
        self.cap = cv2.VideoCapture(self.index)
        self.thread = Thread(target=self.get_camera_status, args=())
        self.set_camera_status()

    def start(self):
        if self.stopped():
            self.toggle_state()
            if self.online and not self.thread.is_alive():
                self.thread = Thread(target=self.update, args=())
                self.thread.daemon = True
                self.thread.start()

    def stop(self):
        if not self.stopped():
            self.toggle_state()
            if self.thread.is_alive():
                self.thread.join()

    def update(self):
        while self.online and not self.stopped():
            self.online, self.frame = self.cap.read()

    def is_opened(self):
        return self.cap.isOpened()

    def get_camera_status(self):
        self.online, self.frame = self.cap.read()

    def set_camera_status(self):
        self.thread = Thread(target=self.get_camera_status, args=())
        self.thread.daemon = True
        self.thread.start()
        time.sleep(1.25)

    def read_frame(self):
        return self.online, self.frame

    def toggle_state(self):
        self.__stopped = not self.__stopped

    def stopped(self):
        return self.__stopped

    def release(self):
        self.cap.release()

    def __del__(self):
        self.release()
