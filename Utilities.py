import os
import sys

import cv2


class CameraUtilities:
    cameras = set()
    MAX_CAMERAS = 100

    @staticmethod
    def get_capture(camera_index):
        return cv2.VideoCapture(camera_index)

    @staticmethod
    def is_camera_timeout(camera_index):
        return not CameraUtilities.get_capture(camera_index).read()[0]

    @staticmethod
    def is_camera_available(camera_index):
        return CameraUtilities.get_capture(camera_index).isOpened()

    @staticmethod
    def add_camera(camera_index):
        if CameraUtilities.is_camera_available(camera_index):
            CameraUtilities.cameras.add(camera_index)

    @staticmethod
    def count_cameras():
        i = 0
        while i <= CameraUtilities.MAX_CAMERAS:
            CameraUtilities.add_camera(i)
            i += 1
        return len(CameraUtilities.cameras)


class PathUtilities:

    @staticmethod
    def get_absolute_path():
        return os.path.abspath(os.path.dirname(sys.argv[0]))

    @staticmethod
    def get_absolute_path_relative(relative_path):
        return os.path.abspath(os.path.join(PathUtilities.get_absolute_path(), relative_path))


class FrameUtilities:

    @staticmethod
    def read_image(image_path):
        return cv2.imread(image_path)

    @staticmethod
    def convert_to_rgb(frame):
        return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    @staticmethod
    def resize_frame(frame, frame_resizing):
        return cv2.resize(frame, (0, 0), fx=frame_resizing, fy=frame_resizing)

    @staticmethod
    def draw_rectangle(frame, location, color, thickness):
        top, right, bottom, left = location
        cv2.rectangle(frame, (left, top), (right, bottom), color, thickness)

    @staticmethod
    def draw_text(frame, text, location, color, font_scale, thickness):
        top, right, bottom, left = location
        cv2.putText(frame, text, (left, top-10), cv2.FONT_HERSHEY_DUPLEX, font_scale, color, thickness)

    @staticmethod
    def create_window(window_name):
        cv2.namedWindow(window_name, cv2.WINDOW_AUTOSIZE)

    @staticmethod
    def show_frame(window_name, frame):
        if frame is not None:
            cv2.imshow(window_name, frame)

    @staticmethod
    def save_frame(frame, file_path, file_name):
        cv2.imwrite(file_path + "/" + file_name, frame)

    @staticmethod
    def is_exit_key_pressed():
        return cv2.waitKey(1) == 27  # ESC

    @staticmethod
    def is_window_visible(window_name):
        return cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) > 0

    @staticmethod
    def encode_frame(frame):
        return cv2.imencode('.ppm', frame)[1].tobytes()

    @staticmethod
    def destroy_window(window_name):
        if FrameUtilities.is_window_visible(window_name):
            cv2.destroyWindow(window_name)

    @staticmethod
    def destroy_all_windows():
        cv2.destroyAllWindows()
