import cv2


class Utilities:
    cameras = []


    @staticmethod
    def is_camera_available(camera_index):
        cap = cv2.VideoCapture(camera_index)
        if cap.read()[0]:
            cap.release()
            return True
        else:
            cap.release()
            return False


    @staticmethod
    def count_cameras():
        i = 0
        while True:
            if Utilities.is_camera_available(i):
                Utilities.cameras.append(i)
                i += 1
            else:
                break
        return i