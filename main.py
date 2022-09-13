from FaceDetector import FaceDetector
from Utilities import Utilities
import sys


def choose_camera():
    camera_index = int(input("Choose the camera index" + str(Utilities.cameras) + " or -1 to exit: "))
    if camera_index == -1:
        sys.exit(0)
    if Utilities.is_camera_available(camera_index):
        return camera_index
    else:
        print("Camera is not available, please choose another camera")
        return choose_camera()


def main():
    path = "images/"
    print("Number of installed cameras is: {}".format(Utilities.count_cameras()))
    camera_index = choose_camera()
    face_detector = FaceDetector(path, camera_index)
    face_detector.detection_loop()
    face_detector.add_face(face_detector.get_absolute_path(path + "another_image/" + "Ahmed Ezzat Nasr.jpg"))
    face_detector.__del__()


if __name__ == "__main__":
    main()
