import cv2


class Utilities:
    cameras = []
    MAX_CAMERAS = 100

    @staticmethod
    def is_camera_available(camera_index):
        cap = cv2.VideoCapture(camera_index)
        result = cap.isOpened()
        if result:
            if not cap.read()[0]:
                result = False
        cap.release()
        return result

    @staticmethod
    def add_camera(camera_index):
        if Utilities.is_camera_available(camera_index):
            Utilities.cameras.append(camera_index)

    @staticmethod
    def count_cameras():
        i = 0
        while i <= Utilities.MAX_CAMERAS:
            Utilities.add_camera(i)
            i += 1
        return len(Utilities.cameras)
