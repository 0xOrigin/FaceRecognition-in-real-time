import glob
import os
import sys
from threading import Lock

import face_recognition
import numpy as np

from Utilities import FrameUtilities


class FaceRecognizer:
    __instance = None
    __acquire_lock = Lock()
    known_face_encodings = []
    known_face_names = []

    def __new__(cls, *args, **kwargs):
        with FaceRecognizer.__acquire_lock:
            if cls.__instance is None:
                cls.__instance = super(FaceRecognizer, cls).__new__(cls)
        return cls.__instance

    def __init__(self, images_path):
        self.abs_path = os.path.abspath(sys.argv[0] + "/..")
        self.images_path = glob.glob(os.path.join(self.abs_path, images_path, "*.*"))
        self.frame_resizing = 1.0

    def load_encoding_images(self):
        self.known_face_encodings.clear()
        self.known_face_names.clear()

        for img_path in self.images_path:
            self.add_known_face_encoding(img_path)
            self.add_known_face_name(img_path)

    def detect_known_faces(self, frame):
        small_frame = FrameUtilities.resize_frame(frame, self.frame_resizing)
        rgb_small_frame = FrameUtilities.convert_to_rgb(small_frame)

        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame, number_of_times_to_upsample=1, model="cnn")
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding, tolerance=0.49)
            name = "Unknown"

            try:
                first_match_index = matches.index(True)
            except Exception as ex:
                first_match_index = -1

            if first_match_index > -1 and matches[first_match_index]:
                name = self.known_face_names[first_match_index]
            face_names.append(name)

        # Convert to numpy array to adjust coordinates with frame resizing quickly
        face_locations = np.array(face_locations)
        face_locations = face_locations / self.frame_resizing

        return face_locations.astype(int), face_names

    def add_known_face_encoding(self, img_path):
        img = FrameUtilities.read_image(img_path)
        rgb_img = FrameUtilities.convert_to_rgb(img)
        img_encoding = face_recognition.face_encodings(rgb_img)[0]
        self.known_face_encodings.append(img_encoding)

    def add_known_face_name(self, img_path):
        basename = os.path.basename(img_path)
        (filename, ext) = os.path.splitext(basename)
        self.known_face_names.append(filename)
