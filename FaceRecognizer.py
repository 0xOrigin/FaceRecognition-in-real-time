import glob
import os
from threading import RLock, Thread
import face_recognition
import numpy as np
import dlib

from Utilities import FrameUtilities, PathUtilities


class FaceRecognizer:
    __instance = None
    __acquire_lock = RLock()
    known_face_encodings = []
    known_face_names = []
    unknown_face_name = "Unknown"
    frame_resizing = 1.0
    number_of_upsample = 1
    model = ["cnn" if dlib.DLIB_USE_CUDA and dlib.cuda.get_num_devices() else "hog"][0]
    tolerance = 0.47

    def __new__(cls, *args, **kwargs):
        with FaceRecognizer.__acquire_lock:
            if cls.__instance is None:
                cls.__instance = super(FaceRecognizer, cls).__new__(cls)
        return cls.__instance

    def load_encoding_images(self, images_path):
        images_path = glob.glob(os.path.join(PathUtilities.get_absolute_path(), images_path, "*.*"))
        for img_path in images_path:
            self.add_face(img_path)
        print("Loaded {} images.".format(len(images_path)))

    @staticmethod
    def get_first_match_index(matches_list):
        try:
            first_match_index = matches_list.index(True)
        except ValueError:
            first_match_index = -1
        return first_match_index

    def detect_known_faces(self, frame):
        small_frame = FrameUtilities.resize_frame(frame, self.frame_resizing)
        rgb_small_frame = FrameUtilities.convert_to_rgb(small_frame)

        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame,
                                                         number_of_times_to_upsample=self.number_of_upsample,
                                                         model=self.model)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding, tolerance=self.tolerance)
            name = self.unknown_face_name

            first_match_index = self.get_first_match_index(matches)
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

    def __add_face(self, img_path):
        with self.__acquire_lock:
            self.add_known_face_encoding(img_path)
            self.add_known_face_name(img_path)

    def add_face(self, img_path):
        thread = Thread(target=self.__add_face, args=(img_path,))
        thread.start()
