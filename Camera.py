import cv2


class Camera:
    def __init__(self, camera_index=0):
        self.cap = cv2.VideoCapture(camera_index)

    def get_capture(self):
        return self.cap

    def is_opened(self):
        return self.cap.isOpened()

    def is_frame_readable(self):
        return self.cap.read()[0]

    def read_frame(self):
        return self.cap.read()[1]

    def release(self):
        self.cap.release()

    def __del__(self):
        self.release()
