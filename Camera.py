import os; os.environ["OPENCV_LOG_LEVEL"] = "SILENT"
from threading import Thread
import cv2


class Camera:
    def __init__(self, camera_index=0):
        self.index = camera_index
        self.online = None
        self.frame = None
        self.stopped = False
        self.cap = cv2.VideoCapture(self.index)
        self.thread = None
        self.set_camera_status()

    def start(self):
        if self.online:
            self.stopped = False
            self.thread = Thread(target=self.update, args=())
            self.thread.daemon = True
            self.thread.start()

    def stop(self):
        self.stopped = True
        if self.thread.is_alive():
            self.thread.join()

    def update(self):
        while self.online and not self.stopped:
            self.online, self.frame = self.cap.read()

    def is_opened(self):
        return self.cap.isOpened()

    def get_camera_status(self):
        self.online, self.frame = self.cap.read()

    def set_camera_status(self):
        self.thread = Thread(target=self.get_camera_status, args=())
        self.thread.daemon = True
        self.thread.start()
        self.thread.join()

    def read_frame(self):
        return self.online, self.frame

    def release(self):
        self.cap.release()

    def __del__(self):
        self.release()
