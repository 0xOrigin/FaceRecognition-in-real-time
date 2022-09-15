from Camera import Camera
import cv2


class CameraUtilities:
    cameras = []
    MAX_CAMERAS = 100

    @staticmethod
    def is_camera_timeout(camera_index):
        return not Camera(camera_index).is_frame_readable()

    @staticmethod
    def is_camera_available(camera_index):
        return Camera(camera_index).is_opened()

    @staticmethod
    def add_camera(camera_index):
        if CameraUtilities.is_camera_available(camera_index):
            CameraUtilities.cameras.append(camera_index)

    @staticmethod
    def count_cameras():
        i = 0
        while i <= CameraUtilities.MAX_CAMERAS:
            CameraUtilities.add_camera(i)
            i += 1
        return len(CameraUtilities.cameras)


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
    def show_frame(window_name, frame):
        cv2.imshow(window_name, frame)

    @staticmethod
    def is_exit_key_pressed():
        return cv2.waitKey(1) == 27  # ESC

    @staticmethod
    def destroy_all_windows():
        cv2.destroyAllWindows()
