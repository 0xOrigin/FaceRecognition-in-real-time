import os; os.environ["OPENCV_LOG_LEVEL"] = "SILENT"
from dataclasses import dataclass
from enum import Enum
from datetime import datetime, timedelta
from Camera import Camera
from Utilities import FrameUtilities
from FaceRecognizer import FaceRecognizer


@dataclass
class Status(Enum):
    Present = 0
    Departed = 1


class FacesDictionary:
    def __init__(self):
        self.dictionary = {}

    def add(self, face_name, time: datetime):
        self.dictionary[face_name] = (Status.Present.name, time)

    def toggle_status(self, face_name, time: datetime):
        self.dictionary[face_name] = ((Status.Present.name, time) if self.dictionary[face_name][0] == Status.Departed.name else (Status.Departed.name, time))

    def is_registered(self, face_name):
        return face_name in self.dictionary


class FaceDetector:
    def __init__(self, images_path, camera_index=0):
        self.face_recognizer = FaceRecognizer(images_path)
        self.face_recognizer.load_encoding_images()
        self.camera = Camera(camera_index)
        self.colors = {"red": (0, 0, 200), "green": (0, 200, 0)}
        self.current_color = self.colors["red"]
        self.detected_faces = FacesDictionary()
        self.number_of_minutes_to_wait = 5
        self.number_of_seconds_to_wait = 5

    def get_absolute_path(self, relative_path):
        return os.path.abspath(os.path.join(self.face_recognizer.abs_path, relative_path))

    def detection_loop(self):
        while True:
            self.detect_faces()
            if FrameUtilities.is_exit_key_pressed():
                break

    def detection_action(self, name):
        if not self.detected_faces.is_registered(name):
            self.detected_faces.add(name, datetime.now())
            print("Welcome: {}".format(name))
        elif datetime.now() - self.detected_faces.dictionary[name][1] >= timedelta(minutes=self.number_of_minutes_to_wait, seconds=self.number_of_seconds_to_wait):
            self.detected_faces.toggle_status(name, datetime.now())
            if self.detected_faces.dictionary[name][0] == Status.Present.name:
                print("Welcome: {} {}".format(name, datetime.now()))
            else:
                print("Goodbye: {} {}".format(name, datetime.now()))
        self.current_color = self.colors["green"]

    def detect_faces(self):
        frame = self.camera.read_frame()
        face_locations, face_names = self.face_recognizer.detect_known_faces(frame)

        for face_loc, name in zip(face_locations, face_names):
            self.current_color = self.colors["red"]

            if name != "Unknown":
                self.detection_action(name)

            FrameUtilities.draw_text(frame, name, face_loc, self.current_color, font_scale=1, thickness=2)
            FrameUtilities.draw_rectangle(frame, face_loc, self.current_color, thickness=4)

        FrameUtilities.show_frame("Face Detector", frame)

    def add_face(self, image_path):
        self.face_recognizer.add_known_face_encoding(image_path)
        self.face_recognizer.add_known_face_name(image_path)
        self.detection_loop()

    def __del__(self):
        self.camera.release()
        FrameUtilities.destroy_all_windows()
