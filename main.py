from FaceDetector import FaceDetector
from Utilities import CameraUtilities
import sys


def choose_camera():
    camera_index = int(input("Choose the camera index" + str(CameraUtilities.cameras) + " or -1 to exit: "))
    if camera_index == -1:
        sys.exit(0)
    if CameraUtilities.is_camera_timeout(camera_index):
        print("Camera is not available, please choose another camera.")
        return choose_camera()
    else:
        return camera_index


def main():
    path = "images/"
    print("Number of installed cameras is: {}.".format(CameraUtilities.count_cameras()))
    print("Cameras are: {}.".format(CameraUtilities.cameras))
    print("------------------------------------------------------------------------------------")
    CameraUtilities.cameras.clear()
    face_detector = FaceDetector(path, CameraUtilities.cameras, window_name="Face Detector")
    face_detector.add_camera(0)
    face_detector.add_camera(1)
    face_detector.start()
    face_detector.add_camera(1)
    face_detector.retest_camera(1)
    face_detector.remove_camera(0)
    face_detector.add_face(face_detector.get_absolute_path(path + "another_image/" + "Ahmed Ezzat Nasr.jpg"))


if __name__ == "__main__":
    main()
