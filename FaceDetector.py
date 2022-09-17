import os
from Camera import Camera
from Utilities import FrameUtilities
from FaceRecognizer import FaceRecognizer
from DetectionRecorder import FacesDictionary, Actions


class FaceDetector:
    def __init__(self, images_path, camera_index=0, window_name="Face Detector"):
        self.face_recognizer = FaceRecognizer(images_path)
        self.face_recognizer.load_encoding_images()
        self.camera = Camera(camera_index)
        self.window_name = window_name + " - Camera: " + str(camera_index)
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
            self.detect_faces()
            if FrameUtilities.is_exit_key_pressed():
                break

    def detection_action(self, name):
        if not self.detected_faces.is_registered(name):
            Actions.register_face(name)
        elif Actions.is_exceeded_waiting_time(name, self.number_of_minutes_to_wait, self.number_of_seconds_to_wait):
            Actions.toggle_status(name)

        self.current_color = self.colors["green"]

    def detect_faces(self):
        is_frame_readable, frame = self.camera.read_frame()
        if is_frame_readable:
            face_locations, face_names = self.face_recognizer.detect_known_faces(frame)

            for face_loc, name in zip(face_locations, face_names):
                self.current_color = self.colors["red"]

                if name != "Unknown":
                    self.detection_action(name)

                FrameUtilities.draw_text(frame, name, face_loc, self.current_color, font_scale=0.7, thickness=2)
                FrameUtilities.draw_rectangle(frame, face_loc, self.current_color, thickness=2)

            FrameUtilities.show_frame(self.window_name, frame)
        else:
            print("Camera {} is not readable".format(self.camera.index))
            self.stop()

    def add_face(self, image_path):
        self.face_recognizer.add_known_face_encoding(image_path)
        self.face_recognizer.add_known_face_name(image_path)
        self.detection_loop()

    def start(self):
        self.stopped = False

    def stop(self):
        self.stopped = True

    def __del__(self):
        self.camera.release()
        FrameUtilities.destroy_all_windows()
