import os; os.environ["OPENCV_LOG_LEVEL"] = "SILENT"
from dataclasses import dataclass
from enum import Enum
from datetime import datetime, timedelta
import cv2
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
        self.cap = cv2.VideoCapture(camera_index)
        self.color_of_rectangle = (0, 0, 200)
        self.detected_faces: FacesDictionary = FacesDictionary()
        self.number_of_minutes_to_wait = 0
        self.number_of_seconds_to_wait = 5

    def get_absolute_path(self, relative_path):
        return os.path.abspath(os.path.join(self.face_recognizer.abs_path, relative_path))

    def detection_loop(self):
        while True:
            self.detect_faces()
            key = cv2.waitKey(1)
            if key == 27:  # ESC
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
        self.color_of_rectangle = (0, 200, 0)

    def detect_faces(self):
        ret, frame = self.cap.read()
        face_locations, face_names = self.face_recognizer.detect_known_faces(frame)

        for face_loc, name in zip(face_locations, face_names):
            top, left, right, bottom = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
            self.color_of_rectangle = (0, 0, 200)
            if name != "Unknown":
                self.detection_action(name)

            cv2.putText(frame, name, (bottom, top - 10), cv2.FONT_HERSHEY_DUPLEX, 1, self.color_of_rectangle, 2)
            cv2.rectangle(frame, (bottom, top), (left, right), self.color_of_rectangle, 4)

        cv2.imshow("Face Detector", frame)

    def add_face(self, image_path):
        self.face_recognizer.add_known_face_encoding(image_path)
        self.face_recognizer.add_known_face_name(image_path)
        self.detection_loop()

    def __del__(self):
        self.cap.release()
        cv2.destroyAllWindows()
