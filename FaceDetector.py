import os
from Camera import Camera
from Utilities import FrameUtilities
from FaceRecognizer import FaceRecognizer
from DetectionRecorder import FacesDictionary, Actions


class FaceDetector:
    def __init__(self, images_path, cameras_indexes: list, window_name="Face Detector"):
        self.face_recognizer = FaceRecognizer(images_path)
        self.face_recognizer.load_encoding_images()
        self.cameras = [Camera(camera_index) for camera_index in cameras_indexes]
        self.window_name = window_name
        self.colors = {"red": (0, 0, 255), "green": (0, 255, 0)}
        self.current_color = self.colors["red"]
        self.detected_faces = FacesDictionary()
        self.number_of_minutes_to_wait = 0
        self.number_of_seconds_to_wait = 10
        self.stopped = False

    def get_absolute_path(self, relative_path):
        return os.path.abspath(os.path.join(self.face_recognizer.abs_path, relative_path))

    def detection_loop(self):
        while not self.stopped:
            for camera in self.cameras:
                self.detect_faces(camera)
            if FrameUtilities.is_exit_key_pressed():
                break

    def detection_action(self, name):
        if not self.detected_faces.is_registered(name):
            Actions.register_face(name)
        elif Actions.is_exceeded_waiting_time(name, self.number_of_minutes_to_wait, self.number_of_seconds_to_wait):
            Actions.toggle_status(name)

        self.current_color = self.colors["green"]

    def detect_faces(self, camera):
        is_frame_readable, frame = camera.read_frame()
        window_name = self.form_window_name(camera.index)
        FrameUtilities.create_window(window_name)

        if is_frame_readable:
            face_locations, face_names = self.face_recognizer.detect_known_faces(frame)

            for face_loc, name in zip(face_locations, face_names):
                self.current_color = self.colors["red"]

                if name != "Unknown":
                    self.detection_action(name)

                FrameUtilities.draw_text(frame, name, face_loc, self.current_color, font_scale=0.7, thickness=2)
                FrameUtilities.draw_rectangle(frame, face_loc, self.current_color, thickness=2)

            FrameUtilities.show_frame(window_name, frame)
        else:
            print("Camera {} is not readable".format(camera.index))
            if FrameUtilities.is_window_visible(window_name):
                FrameUtilities.destroy_window(window_name)
            self.cameras.remove(camera)
            # self.stop()

    def add_face(self, image_path):
        self.face_recognizer.add_known_face_encoding(image_path)
        self.face_recognizer.add_known_face_name(image_path)
        self.detection_loop()

    def start(self):
        self.stopped = False

    def stop(self):
        self.stopped = True

    def form_window_name(self, camera_index):
        return self.window_name + " - Camera: " + str(camera_index)

    def __del__(self):
        for camera in self.cameras:
            camera.release()
        FrameUtilities.destroy_all_windows()
