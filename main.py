from FaceDetectorControl import FaceDetectorControl
from Utilities import CameraUtilities, PathUtilities
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
    face_detector = FaceDetectorControl(path, CameraUtilities.cameras, window_name="Face Detector")
    face_detector.cameras_control.add_camera(0)
    face_detector.cameras_control.add_camera(1)
    face_detector.start()
    face_detector.stop()
    face_detector.cameras_control.retest_camera(0)
    face_detector.add_face(PathUtilities.get_absolute_path_relative(path + "another_image/Ahmed Ezzat Nasr.jpg"))
    face_detector.start()
    face_detector.stop()


if __name__ == "__main__":
    main()
